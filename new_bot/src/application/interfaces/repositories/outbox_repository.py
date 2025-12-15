from typing import Protocol, List
from datetime import datetime
from src.domain.entities.outbox_event import OutboxEvent
from src.domain.value_objects.ids import OutboxEventId

class OutboxRepository(Protocol):
    async def add(self, event: OutboxEvent) -> None:
        ...

    async def list_unpublished(self, limit: int) -> List[OutboxEvent]:
        ...

    async def mark_published(self, outbox_event_id: OutboxEventId, published_at: datetime) -> None:
        ...
