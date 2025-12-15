from typing import Protocol, Optional
from src.domain.entities.user import User
from src.domain.value_objects.ids import UserId, TenantId

class UserRepository(Protocol):
    async def get_by_id(self, user_id: UserId) -> Optional[User]:
        ...

    async def get_by_telegram_id(self, tenant_id: TenantId, telegram_user_id: int) -> Optional[User]:
        ...

    async def add(self, user: User) -> None:
        ...
