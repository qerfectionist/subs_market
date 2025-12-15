from aiogram import Router, types
from aiogram.filters import CommandStart
import logging

logger = logging.getLogger(__name__)
router = Router()

from aiogram.utils.keyboard import ReplyKeyboardBuilder

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    logger.info(f"Start command from {message.from_user.id}")
    
    builder = ReplyKeyboardBuilder()
    builder.button(text="🗂 My Clubs")
    builder.button(text="🔍 Search")
    builder.button(text="➕ Create Club")
    builder.button(text="👤 Profile")
    builder.adjust(2)

    await message.answer(
        "👋 Welcome to Subscription Clubs Bot!\n"
        "(Running in Minimal Safe Mode)\n\n"
        "Please select an option from the menu below:",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
