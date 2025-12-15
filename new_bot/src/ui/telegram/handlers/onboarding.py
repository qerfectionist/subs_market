from aiogram import Router, types
from aiogram.filters import CommandStart
import logging
from aiogram.utils.keyboard import ReplyKeyboardBuilder

logger = logging.getLogger(__name__)
router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    logger.info(f"Start command from {message.from_user.id}")
    
    builder = ReplyKeyboardBuilder()
    builder.button(text="🗂 Мои подписки")
    builder.button(text="🔍 Поиск клубов")
    builder.button(text="➕ Создать клуб")
    builder.button(text="👤 Профиль")
    builder.adjust(2)

    await message.answer(
        "👋 Добро пожаловать в бот совместных подписок!\n\n"
        "Здесь вы можете объединяться в группы для дешевой оплаты сервисов.\n"
        "Пожалуйста, выберите действие в меню ниже:",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
