
from src.domain.entities.dispute import Dispute
from src.domain.entities.dispute_event import DisputeEvent
from ..interfaces.unit_of_work import UnitOfWork
from ..dtos import RaiseDisputeRequest, RaiseDisputeResponse
from src.domain.value_objects.ids import DisputeId, DisputeEventId
import uuid
from datetime import datetime

async def execute(uow: UnitOfWork, request: RaiseDisputeRequest) -> RaiseDisputeResponse:
    async with uow:
        # 1. Create Dispute
        dispute_id = DisputeId(uuid.uuid4())
        dispute = Dispute(
            dispute_id=dispute_id,
            club_id=request.club_id,
            opened_by_user_id=request.user_id,
            opened_at=datetime.utcnow(),
            status="OPEN" # or Enum
        )
        
        await uow.disputes.add(dispute)
        await uow.commit()
        return RaiseDisputeResponse(dispute_id=dispute_id)
