import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

# Import Base and verify models are imported
from src.infrastructure.database.base import Base
# Import all models to ensure they are registered in metadata
from src.infrastructure.database.models import * 

load_dotenv()

async def init_models():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Error: DATABASE_URL not set in .env")
        return

    print(f"Connecting to {database_url}...")
    engine = create_async_engine(database_url, echo=True)

    async with engine.begin() as conn:
        print("Creating tables...")
        # await conn.run_sync(Base.metadata.drop_all) # Optional: Reset DB
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully.")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_models())
