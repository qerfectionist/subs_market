from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import os

# Placeholder for real config. Using env var or default for scaffolding.
def get_async_engine():
    # Load from env provided by caller (who should have called load_dotenv)
    url = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")
    return create_async_engine(url, echo=False)

def get_sessionmaker(engine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
