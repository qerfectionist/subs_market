from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.interfaces.repositories.dispute_repository import DisputeRepository
from src.domain.entities.dispute import Dispute
from src.domain.entities.dispute_event import DisputeEvent
from src.domain.value_objects.ids import DisputeId
from ..models.dispute import DisputeModel
from ..mappers import to_domain_dispute, to_db_dispute, to_db_dispute_event

class DisputeRepositoryImpl(DisputeRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, dispute_id: DisputeId) -> Optional[Dispute]:
        stmt = select(DisputeModel).where(DisputeModel.dispute_id == dispute_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return to_domain_dispute(model) if model else None

    async def add(self, dispute: Dispute) -> None:
        model = to_db_dispute(dispute)
        self._session.add(model)

    async def add_event(self, event: DisputeEvent) -> None:
        model = to_db_dispute_event(event)
        self._session.add(model)
