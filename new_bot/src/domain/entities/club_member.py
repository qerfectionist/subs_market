from dataclasses import dataclass
from datetime import datetime
from ..value_objects.ids import ClubId, UserId

@dataclass(frozen=True)
class ClubMember:
    club_id: ClubId
    user_id: UserId
    joined_at: datetime
    is_owner: bool
