from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.interfaces.repositories.user_repository import UserRepository
from src.domain.entities.user import User
from src.domain.value_objects.ids import UserId, TenantId
from ..models.user import UserModel
from ..mappers import to_domain_user, to_db_user

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: UserId) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.user_id == user_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return to_domain_user(model) if model else None

    async def get_by_telegram_id(self, tenant_id: TenantId, telegram_user_id: int) -> Optional[User]:
        stmt = select(UserModel).where(
            UserModel.tenant_id == tenant_id,
            UserModel.telegram_user_id == telegram_user_id
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return to_domain_user(model) if model else None

    async def add(self, user: User) -> None:
        model = to_db_user(user)
        self._session.add(model)
