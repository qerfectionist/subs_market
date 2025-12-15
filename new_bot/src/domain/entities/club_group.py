from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ..value_objects.ids import ClubId

@dataclass(frozen=True)
class ClubGroup:
    club_id: ClubId
    telegram_chat_id: int
    linked_at: datetime
    invite_link: Optional[str] = None
