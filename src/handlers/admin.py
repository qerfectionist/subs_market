from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from src.config import config

admin_router = Router()
admin_router.message.filter(F.from_user.id.in_(config.ADMIN_IDS))

@admin_router.message(Command("admin"))
async def admin_start(message: Message):
    await message.answer("Admin panel")
