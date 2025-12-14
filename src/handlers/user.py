from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.repo import Repository

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    repo = Repository(session)
    # Note: repo.add_user upserts, so it's safe to call on every start
    user = await repo.add_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username
    )
    await message.answer(f"Hello, {user.full_name}!")
