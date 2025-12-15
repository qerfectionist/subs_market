from src.domain.entities.club_member import ClubMember
from src.domain.value_objects.ids import MemberPeriodId, BillingPeriodId
from ..dtos import JoinClubRequest, JoinClubResponse
from ..errors import NotFoundError, ConflictError
from datetime import datetime
from src.application.interfaces.unit_of_work import UnitOfWork

async def execute(uow: UnitOfWork, request: JoinClubRequest) -> JoinClubResponse:
    async with uow:
        # 1. Check Club exists
        club = await uow.clubs.get_by_id(request.club_id)
        if not club:
            raise NotFoundError("Club not found")

        # 2. Check if already member
        existing_member = await uow.memberships.get_member(request.club_id, request.user_id)
        if existing_member:
            raise ConflictError("Already a member")

        # 3. Create Membership (Pending Approval implementation depends on logic, here we create directly or request)
        # MVP Scope: Direct join or Request? Prompt 9 says "Join Request, Approve/Reject"
        # So we likely create a record with 'pending' status OR just a notification.
        # But ClubMember entity doesn't have status field in current def. 
        # Checking 03_domain_model.md -> ClubMember link exists. 
        # Maybe we assume ClubMember existence = Joined. 
        # If "Request" is needed, we might need a separate JoinRequest entity or a status on ClubMember.
        # For scaffold, assuming we create a Member record but maybe marked as inactive?
        # Or, we strictly follow Prompt 6 "JoinClub" -> ???
        # Let's assume we create the member with a flag or separate list.
        # Given Entity definition, ClubMember has no status.
        # TODO: Clarify Join Request storage. For now, adding to membership directly or Outbox event for owner to approve?
        # Let's assume for MVP: User clicks Join -> Bot notifies Owner -> Owner clicks Approve -> Member added.
        # So "JoinClub" might just send a notification event if strict approval is needed.
        # OR creates a record that is not yet valid.
        
        # Implementation decision: JoinClub creates a 'candidate' or sends request.
        # Since we have ApproveMember use case, we definitely need a state.
        # But ClubMember entity is simple.
        # TODO: Add JoinRequest logic/entity or field.

        new_member = ClubMember(
            club_id=request.club_id,
            user_id=request.user_id,
            joined_at=datetime.utcnow(),
            is_owner=False
        )
        
        # TODO: Only add if approval not required OR add to separate 'requests' table.
        # await uow.memberships.add(new_member) 

        await uow.commit()
        return JoinClubResponse(success=True, status="requested")
