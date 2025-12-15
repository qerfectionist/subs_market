from typing import Optional, List
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.interfaces.repositories.membership_repository import MembershipRepository
from src.domain.entities.club_member import ClubMember
from src.domain.entities.member_period import MemberPeriod
from src.domain.value_objects.ids import ClubId, UserId, MemberPeriodId, BillingPeriodId
from ..models.club_member import ClubMemberModel
from ..models.member_period import MemberPeriodModel
from ..mappers import (
    to_domain_club_member, to_db_club_member,
    to_domain_member_period, to_db_member_period
)

class MembershipRepositoryImpl(MembershipRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_member(self, club_id: ClubId, user_id: UserId) -> Optional[ClubMember]:
        stmt = select(ClubMemberModel).where(
            ClubMemberModel.club_id == club_id,
            ClubMemberModel.user_id == user_id
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return to_domain_club_member(model) if model else None

    async def list_members(self, club_id: ClubId) -> List[ClubMember]:
        stmt = select(ClubMemberModel).where(ClubMemberModel.club_id == club_id)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [to_domain_club_member(m) for m in models]

    async def add(self, member: ClubMember) -> None:
        model = to_db_club_member(member)
        self._session.add(model)

    async def count_members(self, club_id: ClubId) -> int:
        from sqlalchemy import func
        stmt = select(func.count()).select_from(ClubMemberModel).where(ClubMemberModel.club_id == club_id)
        result = await self._session.execute(stmt)
        return result.scalar() or 0

    async def remove(self, club_id: ClubId, user_id: UserId) -> None:
        stmt = delete(ClubMemberModel).where(
            ClubMemberModel.club_id == club_id,
            ClubMemberModel.user_id == user_id
        )
        await self._session.execute(stmt)

    async def get_member_period(self, member_period_id: MemberPeriodId) -> Optional[MemberPeriod]:
        stmt = select(MemberPeriodModel).where(MemberPeriodModel.member_period_id == member_period_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return to_domain_member_period(model) if model else None

    async def add_member_period(self, mp: MemberPeriod) -> None:
        model = to_db_member_period(mp)
        self._session.add(model)

    async def update_member_period(self, mp: MemberPeriod) -> None:
        stmt = update(MemberPeriodModel).where(
            MemberPeriodModel.member_period_id == mp.member_period_id
        ).values(status=mp.status)
        await self._session.execute(stmt)

    async def get_by_period_and_user(self, billing_period_id: BillingPeriodId, user_id: UserId) -> Optional[MemberPeriod]:
        stmt = select(MemberPeriodModel).where(
            MemberPeriodModel.billing_period_id == billing_period_id,
            MemberPeriodModel.user_id == user_id
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return to_domain_member_period(model) if model else None

    async def list_member_periods(self, billing_period_id: BillingPeriodId) -> List[MemberPeriod]:
        stmt = select(MemberPeriodModel).where(
            MemberPeriodModel.billing_period_id == billing_period_id
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [to_domain_member_period(m) for m in models]
