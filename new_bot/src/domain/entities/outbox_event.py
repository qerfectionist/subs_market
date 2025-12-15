from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from ..value_objects.ids import OutboxEventId

@dataclass(frozen=True)
class OutboxEvent:
    outbox_event_id: OutboxEventId
    aggregate_type: str
    aggregate_id: str
    event_type: str
    payload: Dict[str, Any]
    occurred_at: datetime
    published_at: Optional[datetime] = None
