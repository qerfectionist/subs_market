from dataclasses import dataclass
from typing import Optional
from ..value_objects.ids import UserId, TenantId

@dataclass(frozen=True)
class User:
    user_id: UserId
    tenant_id: TenantId
    display_name: str
    telegram_user_id: Optional[int] = None
