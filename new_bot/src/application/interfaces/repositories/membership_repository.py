from typing import Protocol, Optional, List
from src.domain.entities.club_member import ClubMember
from src.domain.entities.member_period import MemberPeriod
from src.domain.value_objects.ids import ClubId, UserId, MemberPeriodId, BillingPeriodId

class MembershipRepository(Protocol):
    async def get_member(self, club_id: ClubId, user_id: UserId) -> Optional[ClubMember]:
        ...

    async def list_members(self, club_id: ClubId) -> List[ClubMember]:
        ...

    async def add(self, member: ClubMember) -> None:
        ...

    async def count_members(self, club_id: ClubId) -> int:
        ...

    async def remove(self, club_id: ClubId, user_id: UserId) -> None:
        ...

    async def get_member_period(self, member_period_id: MemberPeriodId) -> Optional[MemberPeriod]:
        ...

    async def add_member_period(self, mp: MemberPeriod) -> None:
        ...

    async def update_member_period(self, mp: MemberPeriod) -> None:
        ...

    async def get_by_period_and_user(self, billing_period_id: BillingPeriodId, user_id: UserId) -> Optional[MemberPeriod]:
        ...

    async def list_member_periods(self, billing_period_id: BillingPeriodId) -> List[MemberPeriod]:
        ...
