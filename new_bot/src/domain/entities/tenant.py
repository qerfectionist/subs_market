from dataclasses import dataclass
from ..value_objects.ids import TenantId

@dataclass(frozen=True)
class Tenant:
    tenant_id: TenantId
    name: str
