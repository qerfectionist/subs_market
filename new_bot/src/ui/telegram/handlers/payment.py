from aiogram import Router, types, F, Bot
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.application.use_cases import open_billing_period, submit_payment_proof, confirm_payment, ensure_user
from src.application.dtos import (
    OpenBillingPeriodRequest, SubmitPaymentProofRequest, ConfirmPaymentRequest, EnsureUserRequest
)
from src.domain.value_objects.ids import ClubId, TenantId, PaymentProofId
from src.domain.value_objects.screenshot_hash import ScreenshotHash
from src.domain.enums.member_period_status import MemberPeriodStatus
from ..states import SubmitProofStates
from ..presenters import BillingPresenter
import uuid
import logging

logger = logging.getLogger(__name__)
router = Router()

DEFAULT_TENANT_ID = TenantId(uuid.UUID('00000000-0000-0000-0000-000000000001'))

class PaymentCallback(CallbackData, prefix="pay"):
    action: str
    proof_id: str

# --- Open Billing ---
@router.message(Command("open_billing"))
async def cmd_open_billing(message: types.Message, command: CommandObject, uow_factory):
    club_id_str = command.args
    if not club_id_str:
        await message.answer("Usage: /open_billing <club_id>")
        return

    uow = uow_factory()
    ensure_req = EnsureUserRequest(
        tenant_id=DEFAULT_TENANT_ID,
        telegram_user_id=message.from_user.id,
        display_name=message.from_user.full_name or "Unknown"
    )
    user_resp = await ensure_user.execute(uow, ensure_req)
    
    try:
        request = OpenBillingPeriodRequest(
            club_id=ClubId(uuid.UUID(club_id_str)),
            actor_user_id=user_resp.user_id
        )
        
        response = await open_billing_period.execute(uow, request)
        await message.answer(BillingPresenter.present_period_opened(response))
    except Exception as e:
        logger.exception("Error opening billing period")
        await message.answer(f"Error: {str(e)}")

# --- Submit Payment Proof ---
@router.message(Command("pay"))
async def cmd_pay(message: types.Message, command: CommandObject, state: FSMContext):
    club_id_str = command.args
    if not club_id_str:
        await message.answer("Usage: /pay <club_id>\nPlease specify the club you are paying for.")
        return
    
    try:
        club_id = uuid.UUID(club_id_str)
    except ValueError:
        await message.answer("Invalid Club ID format.")
        return

    await state.update_data(club_id=str(club_id))
    await message.answer("Please upload the payment screenshot/receipt.")
    await state.set_state(SubmitProofStates.waiting_for_screenshot)

@router.message(SubmitProofStates.waiting_for_screenshot, F.photo)
async def process_screenshot(message: types.Message, state: FSMContext, uow_factory, bot: Bot):
    photo = message.photo[-1]
    file_id = photo.file_id
    # Use file_unique_id as simple hash for now, better to hash content byte stream if possible, 
    # but unique_id is good enough for Telegram-side dupe check.
    screenshot_hash = ScreenshotHash(photo.file_unique_id)
    
    data = await state.get_data()
    club_id = ClubId(uuid.UUID(data['club_id']))
    
    uow = uow_factory()
    
    ensure_req = EnsureUserRequest(
        tenant_id=DEFAULT_TENANT_ID,
        telegram_user_id=message.from_user.id,
        display_name=message.from_user.full_name or "Unknown"
    )
    user_resp = await ensure_user.execute(uow, ensure_req)
    
    try:
        request = SubmitPaymentProofRequest(
            user_id=user_resp.user_id,
            club_id=club_id,
            file_id=file_id,
            screenshot_hash=screenshot_hash
        )
        
        response = await submit_payment_proof.execute(uow, request)
        await message.answer(BillingPresenter.present_proof_submitted(response))
        
        # Notify Owner
        proof_id_str = str(response.payment_proof_id)
        
        # Get Club Owner ID logic (requires new query or re-querying club)
        async with uow:  # Re-enter or reuse logic? 
            # Ideally execute returns needed info or we query.
            # Querying Club to get Owner User ID, then User to get Telegram ID
            club = await uow.clubs.get_by_id(club_id)
            if club:
                owner = await uow.users.get_by_id(club.owner_user_id)
                if owner:
                    builder = InlineKeyboardBuilder()
                    builder.button(text="✅ Confirm", callback_data=PaymentCallback(action="confirm", proof_id=proof_id_str))
                    builder.button(text="❌ Reject", callback_data=PaymentCallback(action="reject", proof_id=proof_id_str))
                    builder.adjust(2)
                    
                    await bot.send_photo(
                        chat_id=owner.telegram_id,
                        photo=file_id,
                        caption=f"New Payment Proof from {message.from_user.full_name} for {club.title}",
                        reply_markup=builder.as_markup()
                    )
        
    except Exception as e:
        logger.exception("Error processing payment proof")
        await message.answer(f"Error: {str(e)}")
    
    await state.clear()

# --- Confirm Payment Callback ---
@router.callback_query(PaymentCallback.filter())
async def process_confirm_callback(callback: types.CallbackQuery, callback_data: PaymentCallback, uow_factory, bot: Bot):
    action = callback_data.action
    proof_id = PaymentProofId(uuid.UUID(callback_data.proof_id))
    approved = (action == "confirm")
    
    uow = uow_factory()
    
    ensure_req = EnsureUserRequest(
        tenant_id=DEFAULT_TENANT_ID,
        telegram_user_id=callback.from_user.id,
        display_name=callback.from_user.full_name or "Unknown"
    )
    user_resp = await ensure_user.execute(uow, ensure_req)
    
    try:
        request = ConfirmPaymentRequest(
            owner_id=user_resp.user_id,
            payment_proof_id=proof_id,
            approved=approved
        )
        
        response = await confirm_payment.execute(uow, request)
        
        status_text = "Confirmed ✅" if approved else "Rejected ❌"
        await callback.message.edit_caption(
            caption=f"{callback.message.caption}\n\nDecision: {status_text}",
            reply_markup=None
        )
        
        # Notify User?
        # We need the user_id from the proof or member period to notify them via Telegram.
        # This requires traversing back: MP -> User -> Telegram ID.
        # For MVP, skipping notification to keep it simple, or we can fetch it.
        
    except Exception as e:
        await callback.answer(f"Error: {str(e)}", show_alert=True)

    await callback.answer()
