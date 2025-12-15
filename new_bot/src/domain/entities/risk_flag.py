from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ..value_objects.ids import RiskFlagId, ClubId, UserId

@dataclass(frozen=True)
class RiskFlag:
    risk_flag_id: RiskFlagId
    type: str
    severity: int
    created_at: datetime
    club_id: Optional[ClubId] = None
    user_id: Optional[UserId] = None
