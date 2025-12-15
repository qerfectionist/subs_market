from typing import List
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.interfaces.repositories.outbox_repository import OutboxRepository
from src.domain.entities.outbox_event import OutboxEvent
from src.domain.value_objects.ids import OutboxEventId
from ..models.outbox_event import OutboxEventModel
from ..mappers import to_domain_outbox_event, to_db_outbox_event

class OutboxRepositoryImpl(OutboxRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, event: OutboxEvent) -> None:
        model = to_db_outbox_event(event)
        self._session.add(model)

    async def list_unpublished(self, limit: int) -> List[OutboxEvent]:
        stmt = select(OutboxEventModel).where(
            OutboxEventModel.published_at.is_(None)
        ).order_by(OutboxEventModel.occurred_at).limit(limit)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [to_domain_outbox_event(m) for m in models]

    async def mark_published(self, outbox_event_id: OutboxEventId, published_at: datetime) -> None:
        stmt = update(OutboxEventModel).where(
            OutboxEventModel.outbox_event_id == outbox_event_id
        ).values(published_at=published_at)
        await self._session.execute(stmt)
