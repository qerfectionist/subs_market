from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any
from ..value_objects.ids import DisputeEventId, DisputeId, UserId

@dataclass(frozen=True)
class DisputeEvent:
    dispute_event_id: DisputeEventId
    dispute_id: DisputeId
    actor_user_id: UserId
    type: str
    payload: Dict[str, Any]
    created_at: datetime
