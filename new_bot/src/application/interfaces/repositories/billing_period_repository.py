from typing import Protocol, Optional
from src.domain.entities.billing_period import BillingPeriod
from src.domain.value_objects.ids import BillingPeriodId, ClubId
from src.domain.value_objects.billing_month import BillingMonth

class BillingPeriodRepository(Protocol):
    async def get_by_id(self, billing_period_id: BillingPeriodId) -> Optional[BillingPeriod]:
        ...

    async def get_by_club_and_month(self, club_id: ClubId, month: BillingMonth) -> Optional[BillingPeriod]:
        ...

    async def get_latest_period(self, club_id: ClubId) -> Optional[BillingPeriod]:
        ...

    async def add(self, period: BillingPeriod) -> None:
        ...

    async def update(self, period: BillingPeriod) -> None:
        ...
