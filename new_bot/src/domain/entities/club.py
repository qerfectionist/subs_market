from dataclasses import dataclass
from ..value_objects.ids import ClubId, TenantId, UserId, ServiceId, TariffId
from ..value_objects.money_kzt import MoneyKZT
from ..enums.club_status import ClubStatus

@dataclass(frozen=True)
class Club:
    club_id: ClubId
    tenant_id: TenantId
    owner_user_id: UserId
    service_id: ServiceId
    tariff_id: TariffId
    title: str
    price: MoneyKZT
    status: ClubStatus
    short_code: str | None = None
