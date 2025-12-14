from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from .models import User

class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, telegram_id: int, full_name: str, username: str = None) -> User:
        """
        Add a new user or update existing one (upsert).
        """
        stmt = insert(User).values(
            telegram_id=telegram_id, 
            full_name=full_name,
            username=username
        ).on_conflict_do_update(
            index_elements=[User.telegram_id],
            set_=dict(full_name=full_name, username=username)
        ).returning(User)
        
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()
        
    async def get_user(self, telegram_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
