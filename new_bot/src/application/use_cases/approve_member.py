from src.domain.entities.club_member import ClubMember
from ..dtos import ApproveMemberRequest, ApproveMemberResponse
from ..errors import PermissionDeniedError, NotFoundError

async def execute(uow: UnitOfWork, request: ApproveMemberRequest) -> ApproveMemberResponse:
    async with uow:
        # 1. Verify Owner
        club = await uow.clubs.get_by_id(request.club_id)
        if not club:
            raise NotFoundError("Club not found")
        
        if club.owner_user_id != request.owner_id:
            raise PermissionDeniedError("Only owner can approve members")

        if request.approved:
            # TODO: Finalize membership creation (if JoinClub created a request)
            # member = ...
            # await uow.memberships.add(member)
            pass
        else:
            # TODO: Reject request
            pass

        await uow.commit()
        return ApproveMemberResponse(success=True)
