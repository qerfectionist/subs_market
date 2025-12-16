from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from src.application.use_cases import get_user_clubs, ensure_user, search_clubs
from src.application.dtos import GetUserClubsRequest, EnsureUserRequest
from src.domain.value_objects.ids import TenantId
from ..presenters import ClubPresenter
from ..i18n import get_text
import uuid
import logging

logger = logging.getLogger(__name__)
router = Router()

DEFAULT_TENANT_ID = TenantId(uuid.UUID('00000000-0000-0000-0000-000000000001'))

class ClubCallback(CallbackData, prefix="club"):
    action: str
    club_id: str

class SearchCallback(CallbackData, prefix="search"):
    action: str
    category: str # "all", "video", "music"
    free_slots: bool = False

@router.message(F.text == "🗂 Мои подписки")
@router.message(Command("my_clubs"))
async def cmd_my_clubs(message: types.Message, uow_factory):
    uow = uow_factory()
    # Ensure user exists first
    # Ensure user exists first (and get UUID)
    user_resp = await ensure_user.execute(uow, EnsureUserRequest(
        tenant_id=DEFAULT_TENANT_ID,
        telegram_user_id=message.from_user.id,
        display_name=message.from_user.full_name or message.from_user.username or "User"
    ))
    
    resp = await get_user_clubs.execute(uow, GetUserClubsRequest(user_id=user_resp.user_id))
    
    if not resp.clubs:
        await message.answer(get_text("my_clubs_empty", message.from_user.language_code))
        return

    # Show list as buttons
    builder = InlineKeyboardBuilder()
    for club in resp.clubs:
        # Status icon
        status_icon = "🟢" if club.status.value == "active" else "🔴"
        btn_text = f"{status_icon} {club.title}"
        builder.button(text=btn_text, callback_data=ClubCallback(action="view", club_id=str(club.club_id)))
    
    builder.adjust(1)
    await message.answer(get_text("my_clubs_title", message.from_user.language_code), reply_markup=builder.as_markup())


@router.message(F.text == "🔍 Поиск клубов")
@router.message(Command("search"))
async def cmd_search(message: types.Message):
    lang = message.from_user.language_code
    builder = InlineKeyboardBuilder()
    
    # Categories default to free_slots=False
    builder.button(text=get_text("btn_video", lang), callback_data=SearchCallback(action="list", category="VIDEO", free_slots=False))
    builder.button(text=get_text("btn_music", lang), callback_data=SearchCallback(action="list", category="MUSIC", free_slots=False))
    builder.button(text=get_text("btn_all", lang), callback_data=SearchCallback(action="list", category="ALL", free_slots=False))
    
    # Toggle Button for Free Slots (Only)
    builder.button(text="✅ Only Free Slots", callback_data=SearchCallback(action="list", category="ALL", free_slots=True))
    
    builder.adjust(2, 1) # 2 cols for cats, 1 for Free Slots
    
    await message.answer(get_text("search_title", lang), reply_markup=builder.as_markup())


@router.message(F.text == "💳 Купить мегабайты")
async def cmd_buy_megabytes(message: types.Message):
    await message.answer("Feature coming soon! 🚀")


@router.callback_query(SearchCallback.filter(F.action == "list"))
async def process_search_category(callback: types.CallbackQuery, callback_data: SearchCallback, uow_factory):
    lang = callback.from_user.language_code
    category = callback_data.category if callback_data.category != "ALL" else None
    only_free = callback_data.free_slots
    
    uow = uow_factory()
    
    # Pass only_free_slots
    resp = await search_clubs.execute(uow, SearchClubsRequest(category=category, only_free_slots=only_free))
    
    if not resp.clubs:
        msg = f"No clubs found in category: {callback_data.category}"
        if only_free:
            msg += " (Free Slots Only)"
        
        # Back button
        builder = InlineKeyboardBuilder()
        builder.button(text="🔙 Back", callback_data=SearchCallback(action="reset", category="ALL", free_slots=False))
        await callback.message.edit_text(msg, reply_markup=builder.as_markup())
        return

    builder = InlineKeyboardBuilder()
    for club in resp.clubs:
        # Include slots info in button text if possible, e.g. "Club (1/5)"
        # But we don't have member count in Club entity easily available without extra query?
        # ClubRepository.search returns List[Club]. Club entity has members_count? 
        # Checking Club Entity... (Step 1579 lists domain entities).
        # Assuming we just show title + price.
        btn_text = f"{club.title} | {club.price.amount} ₸"
        builder.button(text=btn_text, callback_data=ClubCallback(action="view", club_id=str(club.club_id)))
    
    # Pagination or Back button?
    builder.button(text="🔙 Back", callback_data=SearchCallback(action="reset", category="ALL", free_slots=False))
    builder.adjust(1)
    
    cat_display = category or "ALL"
    if only_free:
        cat_display += " (Free)"
        
    await callback.message.edit_text(
        text=get_text("search_found", lang, count=len(resp.clubs), category=cat_display),
        reply_markup=builder.as_markup()
    )

# Handle Reset/Back
@router.callback_query(SearchCallback.filter(F.action == "reset"))
async def process_search_reset(callback: types.CallbackQuery):
    lang = callback.from_user.language_code
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text("btn_video", lang), callback_data=SearchCallback(action="list", category="VIDEO", free_slots=False))
    builder.button(text=get_text("btn_music", lang), callback_data=SearchCallback(action="list", category="MUSIC", free_slots=False))
    builder.button(text=get_text("btn_all", lang), callback_data=SearchCallback(action="list", category="ALL", free_slots=False))
    builder.button(text="✅ Only Free Slots", callback_data=SearchCallback(action="list", category="ALL", free_slots=True))
    builder.adjust(2, 1)
    
    await callback.message.edit_text(get_text("search_title", lang), reply_markup=builder.as_markup())

from src.application.use_cases import get_club_details
from src.application.dtos import GetClubDetailsRequest
from src.domain.value_objects.ids import ClubId

@router.callback_query(ClubCallback.filter(F.action == "view"))
async def process_club_view(callback: types.CallbackQuery, callback_data: ClubCallback, uow_factory):
    lang = callback.from_user.language_code
    uow = uow_factory()
    
    resp = await get_club_details.execute(uow, GetClubDetailsRequest(club_id=ClubId(uuid.UUID(callback_data.club_id))))
    
    if not resp:
        await callback.answer("Club not found", show_alert=True)
        return

    club = resp.club
    
    # Text formatting
    details_text = (
        f"<b>{club.title}</b>\n\n"
        f"{get_text('club_price', lang, amount=club.price.amount)}\n"
        f"{get_text('club_members', lang, count=resp.member_count, capacity=resp.tariff_capacity)}\n"
        f"{get_text('club_status', lang, status=club.status.value)}\n"
        f"{get_text('club_id', lang, club_id=club.club_id)}"
    )
    
    builder = InlineKeyboardBuilder()
    # Actions
    builder.button(text=get_text("btn_back", lang), callback_data=SearchCallback(action="list", category="ALL", free_slots=False))
    # builder.button(text="⚙️ Settings", callback_data=...) # Todo
    builder.adjust(1)
    
    await callback.message.edit_text(
        text=details_text,
        reply_markup=builder.as_markup()
    )




@router.message(F.text == "👤 Профиль")
@router.message(Command("profile"))
async def cmd_profile(message: types.Message):
    user = message.from_user
    await message.answer(
        f"👤 <b>Профиль пользователя</b>\n\n"
        f"ID: <code>{user.id}</code>\n"
        f"Имя: {user.full_name}\n"
        f"Username: @{user.username or 'Не указан'}"
    )
