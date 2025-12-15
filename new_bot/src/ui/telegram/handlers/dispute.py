from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from src.application.use_cases import raise_dispute, resolve_dispute, ensure_user
from src.application.dtos import RaiseDisputeRequest, ResolveDisputeRequest, EnsureUserRequest
from src.domain.value_objects.ids import ClubId, DisputeId, TenantId
from ..states import RaiseDisputeStates
import uuid
import logging

logger = logging.getLogger(__name__)
router = Router()

DEFAULT_TENANT_ID = TenantId(uuid.UUID('00000000-0000-0000-0000-000000000001'))

@router.message(Command("dispute"))
async def cmd_dispute(message: types.Message, state: FSMContext):
    await message.answer("What is the reason for the dispute?")
    await state.set_state(RaiseDisputeStates.waiting_for_reason)

@router.message(RaiseDisputeStates.waiting_for_reason)
async def process_dispute_reason(message: types.Message, state: FSMContext, uow_factory):
    reason = message.text
    
    uow = uow_factory()
    ensure_req = EnsureUserRequest(
        tenant_id=DEFAULT_TENANT_ID,
        telegram_user_id=message.from_user.id,
        display_name=message.from_user.full_name or "Unknown"
    )
    user_resp = await ensure_user.execute(uow, ensure_req)
    logger.info(f"RaiseDispute: tg_id={message.from_user.id} user_id={user_resp.user_id}")
    
    # Placeholder ClubId
    request = RaiseDisputeRequest(
        user_id=user_resp.user_id,
        club_id=ClubId(uuid.uuid4()), 
        reason=reason
    )
    
    await raise_dispute.execute(uow, request)
    await message.answer("Dispute opened successfully.")
    await state.clear()
