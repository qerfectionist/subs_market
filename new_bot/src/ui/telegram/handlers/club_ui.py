from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from src.application.use_cases import get_user_clubs, ensure_user
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

# --- My Clubs ---

@router.message(F.text == "🗂 My Clubs")
@router.message(Command("my_clubs"))
async def cmd_my_clubs(message: types.Message, uow_factory):
    lang = message.from_user.language_code
    # ... existing implementation ...
    uow = uow_factory()
    ensure_req = EnsureUserRequest(
        tenant_id=DEFAULT_TENANT_ID,
        telegram_user_id=message.from_user.id,
        display_name=message.from_user.full_name or "Unknown"
    )
    user_resp = await ensure_user.execute(uow, ensure_req)
    
    req = GetUserClubsRequest(user_id=user_resp.user_id)
    resp = await get_user_clubs.execute(uow, req)
    
    markup = None
    if resp.clubs:
        builder = InlineKeyboardBuilder()
        for club in resp.clubs:
             btn_text = f"{club.title} | {club.price.amount} ₸"
             builder.button(text=btn_text, callback_data=ClubCallback(action="view", club_id=str(club.club_id)))
        builder.adjust(1)
        markup = builder.as_markup()
        
    await message.answer(
        text=ClubPresenter.present_club_list(resp.clubs, lang),
        reply_markup=markup
    )

@router.message(F.text == "🔍 Search")
@router.message(Command("search"))
async def cmd_search(message: types.Message):
    lang = message.from_user.language_code
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text("btn_video", lang), callback_data=SearchCallback(action="list", category="VIDEO"))
    builder.button(text=get_text("btn_music", lang), callback_data=SearchCallback(action="list", category="MUSIC"))
    builder.button(text=get_text("btn_all", lang), callback_data=SearchCallback(action="list", category="ALL"))
    builder.adjust(2)
    
    await message.answer(get_text("search_title", lang), reply_markup=builder.as_markup())

from src.application.use_cases import search_clubs
from src.application.dtos import SearchClubsRequest

@router.callback_query(SearchCallback.filter(F.action == "list"))
async def process_search_category(callback: types.CallbackQuery, callback_data: SearchCallback, uow_factory):
    lang = callback.from_user.language_code
    category = callback_data.category if callback_data.category != "ALL" else None
    
    uow = uow_factory()
    
    resp = await search_clubs.execute(uow, SearchClubsRequest(category=category))
    
    if not resp.clubs:
        await callback.message.edit_text(f"No clubs found in category: {callback_data.category}")
        return

    builder = InlineKeyboardBuilder()
    for club in resp.clubs:
        btn_text = f"{club.title} | {club.price.amount} ₸"
        # View action reuses ClubCallback
        builder.button(text=btn_text, callback_data=ClubCallback(action="view", club_id=str(club.club_id)))
    builder.adjust(1)
    
    cat_display = category or "ALL"
    await callback.message.edit_text(
        text=get_text("search_found", lang, count=len(resp.clubs), category=cat_display),
        reply_markup=builder.as_markup()
    )

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
        f"💰 Price: {club.price.amount} ₸\n"
        f"👥 Members: {resp.member_count} / {resp.tariff_capacity}\n"
        f"ℹ️ Status: {club.status.value}\n"
        f"🆔 ID: <code>{club.club_id}</code>"
    )
    
    builder = InlineKeyboardBuilder()
    # Actions
    builder.button(text="🔙 Back", callback_data=SearchCallback(action="list", category="ALL")) # Simple back to search/list
    # builder.button(text="⚙️ Settings", callback_data=...) # Todo
    builder.adjust(1)
    
    await callback.message.edit_text(
        text=details_text,
        reply_markup=builder.as_markup()
    )
