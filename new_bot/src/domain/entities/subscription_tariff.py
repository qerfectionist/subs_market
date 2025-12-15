from dataclasses import dataclass
from ..value_objects.ids import TariffId, ServiceId

@dataclass(frozen=True)
class SubscriptionTariff:
    tariff_id: TariffId
    service_id: ServiceId
    name: str
    capacity: int
    currency: str = "KZT"
    is_active: bool = True
