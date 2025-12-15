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
    # Shared processors
    processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    
    # Renderer selection
    if config.DEBUG:
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        processors.append(structlog.processors.JSONRenderer())

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
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
