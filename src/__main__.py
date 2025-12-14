import asyncio
import structlog
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from src.config import config
from src.handlers import user, admin
from src.middlewares.db_session import DbSessionMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

logger = structlog.get_logger()

async def main():
    # Basic logging config
    structlog.configure(
        processors=[
            structlog.processors.JSONRenderer()
        ]
    )
    
    # Dependencies
    engine = create_async_engine(config.database_url, echo=True)
    session_pool = async_sessionmaker(engine, expire_on_commit=False)
    
    redis = Redis.from_url(config.redis_url)
    storage = RedisStorage(redis=redis)
    # from aiogram.fsm.storage.memory import MemoryStorage
    # storage = MemoryStorage()
    
    bot = Bot(token=config.BOT_TOKEN.get_secret_value())
    dp = Dispatcher(storage=storage)
    
    # Middlewares
    dp.update.middleware(DbSessionMiddleware(session_pool=session_pool))
    
    # Routers
    dp.include_router(admin.admin_router)
    dp.include_router(user.user_router)
    
    # Start
    logger.info("Starting bot...")
    try:
        await dp.start_polling(bot)
    finally:
        await engine.dispose()
        await redis.close()

if __name__ == "__main__":
    asyncio.run(main())
