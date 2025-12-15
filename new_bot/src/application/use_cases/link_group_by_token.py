from src.domain.entities.club_group import ClubGroup
from src.domain.value_objects.ids import ClubId
from ..interfaces.unit_of_work import UnitOfWork
from ..dtos import LinkGroupRequest, LinkGroupResponse
from ..errors import NotFoundError, PermissionDeniedError
from datetime import datetime

async def execute(uow: UnitOfWork, request: LinkGroupRequest) -> LinkGroupResponse:
    async with uow:
        # 1. Find Club by token
        # TODO: Implement token lookup mechanism
        # club_id = await uow.tokens.get_club_by_token(request.token)
        # Placeholder:
        club = None # await uow.clubs.get_by_token(...) 
        if not club:
            raise NotFoundError("Invalid or expired token")

        # 2. Verify Owner
        if club.owner_user_id != request.user_id:
            raise PermissionDeniedError("Not club owner")

        # 3. Check Chat ID uniqueness
        # existing_group = await uow.clubs.get_group_by_chat_id(request.chat_id)
        # if existing_group: raise ConflictError(...)

        # 4. Create ClubGroup
        group = ClubGroup(
            club_id=club.club_id,
            telegram_chat_id=request.chat_id,
            linked_at=datetime.utcnow(),
            invite_link=request.invite_link
        )
        # TODO: Add group to repo
        # await uow.clubs.add_group(group)

        # 5. Invalidate Token
        # TODO: await uow.tokens.invalidate(request.token)

        # 6. Emit Event
        # event = OutboxEvent(...)
        # await uow.outbox.add(event)

        await uow.commit()
        return LinkGroupResponse(club_id=club.club_id, success=True)
