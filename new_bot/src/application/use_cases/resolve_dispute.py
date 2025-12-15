from ..interfaces.unit_of_work import UnitOfWork
from ..dtos import ResolveDisputeRequest, ResolveDisputeResponse
from ..errors import NotFoundError
from src.domain.entities.dispute_event import DisputeEvent
from src.domain.value_objects.ids import DisputeEventId
from src.domain.enums.club_status import ClubStatus # Corrected typo: 'ClubStatusndError' -> 'ClubStatus'

async def execute(uow: UnitOfWork, request: ResolveDisputeRequest) -> ResolveDisputeResponse:
    async with uow:
        dispute = await uow.disputes.get_by_id(request.dispute_id)
        if not dispute:
            raise NotFoundError("Dispute not found")

        # Update status
        # dispute.status = request.status
        # await uow.disputes.update(dispute)

        await uow.commit()
        return ResolveDisputeResponse(success=True)
