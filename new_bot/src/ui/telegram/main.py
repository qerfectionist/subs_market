import asyncio
import logging
import os
import sys

# SAFETY GUARD: Prevent running on incompatible Python 3.14+
if sys.version_info >= (3, 14):
    print("❌ ERROR: Python 3.14+ is not supported due to Aiogram incompatibility.")
    print(f"   Current version: {sys.version}")
    print("   Required: Python 3.11 or 3.12")
    print("   Please install Python 3.12 from https://www.python.org/downloads/")
    sys.exit(1)

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from src.ui.telegram.handlers import onboarding, club, payment, dispute, club_ui
from src.infrastructure.database.session import get_async_engine, get_sessionmaker
from src.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork
from src.ui.telegram.middlewares.uow_factory import UoWFactoryMiddleware

async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Load env manually just in case
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is missing!")
        return

    # Infrastructure
    engine = get_async_engine()
    sessionmaker = get_sessionmaker(engine)
    
    # Factory for UoW
    def uow_factory():
        return SqlAlchemyUnitOfWork(sessionmaker)

    # Bot Init
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Middleware
    dp.update.middleware(UoWFactoryMiddleware(uow_factory))

    # Routers
    dp.include_router(onboarding.router)
    dp.include_router(club.router)
    dp.include_router(payment.router)
    dp.include_router(club_ui.router)
    if hasattr(dispute, 'router'):
        dp.include_router(dispute.router)

    # Setup Commands
    await setup_bot_commands(bot)

    logger.info("Starting Symbiosis Bot (Full Mode)...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await engine.dispose()

async def setup_bot_commands(bot: Bot):
    from aiogram.types import BotCommand
    commands = [
        BotCommand(command="start", description="Главное меню"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="my_clubs", description="Мои клубы"),
        BotCommand(command="search", description="Поиск клубов"),
        BotCommand(command="support", description="AI-поддержка"),
        BotCommand(command="admin", description="Панель администратора"),
    ]
    await bot.set_my_commands(commands)

if __name__ == "__main__":
    asyncio.run(main())
