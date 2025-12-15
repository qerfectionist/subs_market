from typing import Protocol, Optional
from src.domain.entities.dispute import Dispute
from src.domain.entities.dispute_event import DisputeEvent
from src.domain.value_objects.ids import DisputeId

class DisputeRepository(Protocol):
    async def get_by_id(self, dispute_id: DisputeId) -> Optional[Dispute]:
        ...

    async def add(self, dispute: Dispute) -> None:
        ...

    async def add_event(self, event: DisputeEvent) -> None:
        ...
