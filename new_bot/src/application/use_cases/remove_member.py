from ..interfaces.unit_of_work import UnitOfWork
from ..dtos import RemoveMemberRequest, RemoveMemberResponse
from ..errors import NotFoundError, PermissionDeniedError
from src.domain.entities.outbox_event import OutboxEvent

async def execute(uow: UnitOfWork, request: RemoveMemberRequest) -> RemoveMemberResponse:
    async with uow:
        # 1. Verify Club and Owner
        club = await uow.clubs.get_by_id(request.club_id)
        if not club:
            raise NotFoundError("Club not found")
        
        if club.owner_user_id != request.owner_id:
            raise PermissionDeniedError("Not owner")

        # 2. Mark Membership as Removed or Delete?
        # Typically set status REMOVED in current period and remove from future.
        # await uow.memberships.remove(request.club_id, request.target_user_id)
        
        await uow.commit()
        return RemoveMemberResponse(success=True)
