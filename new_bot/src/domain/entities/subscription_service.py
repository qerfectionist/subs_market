from dataclasses import dataclass
from ..value_objects.ids import ServiceId, TenantId

@dataclass(frozen=True)
class SubscriptionService:
    service_id: ServiceId
    tenant_id: TenantId
    name: str
    category: str # e.g. "VIDEO", "MUSIC"
    is_active: bool
