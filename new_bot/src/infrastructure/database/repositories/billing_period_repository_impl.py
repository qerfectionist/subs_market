from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.interfaces.repositories.billing_period_repository import BillingPeriodRepository
from src.domain.entities.billing_period import BillingPeriod
from src.domain.value_objects.ids import BillingPeriodId, ClubId
from ....domain.value_objects.billing_month import BillingMonth
from ..models.billing_period import BillingPeriodModel
from ..mappers import to_domain_billing_period, to_db_billing_period

class BillingPeriodRepositoryImpl(BillingPeriodRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, billing_period_id: BillingPeriodId) -> Optional[BillingPeriod]:
        stmt = select(BillingPeriodModel).where(BillingPeriodModel.billing_period_id == billing_period_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return to_domain_billing_period(model) if model else None

    async def get_by_club_and_month(self, club_id: ClubId, month: BillingMonth) -> Optional[BillingPeriod]:
        stmt = select(BillingPeriodModel).where(
            BillingPeriodModel.club_id == club_id,
            BillingPeriodModel.year == month.year,
            BillingPeriodModel.month == month.month
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return to_domain_billing_period(model) if model else None

    async def get_latest_period(self, club_id: ClubId) -> Optional[BillingPeriod]:
        stmt = select(BillingPeriodModel).where(
            BillingPeriodModel.club_id == club_id
        ).order_by(
            BillingPeriodModel.year.desc(), BillingPeriodModel.month.desc()
        ).limit(1)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return to_domain_billing_period(model) if model else None

    async def add(self, period: BillingPeriod) -> None:
        model = to_db_billing_period(period)
        self._session.add(model)

    async def update(self, period: BillingPeriod) -> None:
        stmt = update(BillingPeriodModel).where(
            BillingPeriodModel.billing_period_id == period.billing_period_id
        ).values(
            status=period.status,
            price_amount=period.price.amount
        )
        await self._session.execute(stmt)
