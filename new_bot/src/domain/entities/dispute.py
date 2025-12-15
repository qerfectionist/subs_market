from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union
from ..value_objects.ids import DisputeId, ClubId, BillingPeriodId, UserId

@dataclass(frozen=True)
class Dispute:
    dispute_id: DisputeId
    club_id: ClubId
    opened_by_user_id: UserId
    opened_at: datetime
    status: str 
    billing_period_id: Optional[BillingPeriodId] = None
