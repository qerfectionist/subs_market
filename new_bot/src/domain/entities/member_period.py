from dataclasses import dataclass
from ..value_objects.ids import MemberPeriodId, BillingPeriodId, ClubId, UserId
from ..enums.member_period_status import MemberPeriodStatus

@dataclass(frozen=True)
class MemberPeriod:
    member_period_id: MemberPeriodId
    billing_period_id: BillingPeriodId
    club_id: ClubId
    user_id: UserId
    status: MemberPeriodStatus
