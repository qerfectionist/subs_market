from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from src.application.use_cases import create_club, link_group_by_token, join_club, ensure_user
from src.application.dtos import CreateClubRequest, LinkGroupRequest, JoinClubRequest, EnsureUserRequest
from src.domain.value_objects.ids import TenantId, ServiceId, TariffId, UserId, ClubId
from src.domain.value_objects.money_kzt import MoneyKZT
from src.domain.value_objects.one_time_token import OneTimeToken
from ..states import CreateClubStates
from ..presenters import ClubPresenter
import uuid
import logging

logger = logging.getLogger(__name__)
router = Router()

DEFAULT_TENANT_ID = TenantId(uuid.UUID('00000000-0000-0000-0000-000000000001'))
DEFAULT_SERVICE_ID = ServiceId(uuid.UUID('00000000-0000-0000-0000-000000000002'))
DEFAULT_TARIFF_ID = TariffId(uuid.UUID('00000000-0000-0000-0000-000000000003'))

# --- Create Club Flow ---
@router.message(Command("create_club"))
async def start_create_club(message: types.Message, state: FSMContext):
    await message.answer("Let's create a club. Please enter the Club Title:")
    await state.set_state(CreateClubStates.waiting_for_title)

@router.message(CreateClubStates.waiting_for_title)
async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Enter the monthly subscription price (KZT):")
    await state.set_state(CreateClubStates.waiting_for_price)

@router.message(CreateClubStates.waiting_for_price)
async def process_price(message: types.Message, state: FSMContext, uow_factory):
    try:
        price = int(message.text)
        if price < 0: raise ValueError
    except ValueError:
        await message.answer("Invalid price. Please enter a positive number.")
        return

    data = await state.get_data()
    title = data['title']
    
    uow = uow_factory()
    
    # Ensure User
    ensure_req = EnsureUserRequest(
        tenant_id=DEFAULT_TENANT_ID,
        telegram_user_id=message.from_user.id,
        display_name=message.from_user.full_name or "Unknown"
    )
    user_resp = await ensure_user.execute(uow, ensure_req)
    logger.info(f"CreateClub: tg_id={message.from_user.id} user_id={user_resp.user_id} is_new={user_resp.is_new}")
    
    request = CreateClubRequest(
        user_id=user_resp.user_id,
        tenant_id=DEFAULT_TENANT_ID,
        service_id=DEFAULT_SERVICE_ID,
        tariff_id=DEFAULT_TARIFF_ID,
        title=title,
        price=MoneyKZT(price)
    )
    
    response = await create_club.execute(uow, request)
    await message.answer(ClubPresenter.present_created(response))
    await state.clear()

# --- Link Group ---
@router.message(Command("link_group"))
async def cmd_link_group(message: types.Message, command: CommandObject, uow_factory):
    token_arg = command.args
    if not token_arg:
        await message.answer("Usage: /link_group <token>")
        return

    uow = uow_factory()
    
    # Ensure User
    ensure_req = EnsureUserRequest(
        tenant_id=DEFAULT_TENANT_ID,
        telegram_user_id=message.from_user.id,
        display_name=message.from_user.full_name or "Unknown"
    )
    user_resp = await ensure_user.execute(uow, ensure_req)
    logger.info(f"LinkGroup: tg_id={message.from_user.id} user_id={user_resp.user_id}")
    
    request = LinkGroupRequest(
        user_id=user_resp.user_id,
        chat_id=message.chat.id,
        token=OneTimeToken(token_arg),
        invite_link=None 
    )
    
    response = await link_group_by_token.execute(uow, request)
    await message.answer(ClubPresenter.present_linked(response))

# --- Join Club ---
@router.message(Command("join"))
async def cmd_join(message: types.Message, command: CommandObject, uow_factory):
    club_id_str = command.args
    if not club_id_str:
        await message.answer("Usage: /join <club_id>")
        return

    uow = uow_factory()
    try:
        club_id = ClubId(uuid.UUID(club_id_str))
    except ValueError:
        await message.answer("Invalid Club ID format.")
        return

    # Ensure User
    ensure_req = EnsureUserRequest(
        tenant_id=DEFAULT_TENANT_ID,
        telegram_user_id=message.from_user.id,
        display_name=message.from_user.full_name or "Unknown"
    )
    user_resp = await ensure_user.execute(uow, ensure_req)
    logger.info(f"JoinClub: tg_id={message.from_user.id} user_id={user_resp.user_id}")

    request = JoinClubRequest(
        user_id=user_resp.user_id,
        club_id=club_id
    )
    
    response = await join_club.execute(uow, request)
    await message.answer(ClubPresenter.present_joined(response))
