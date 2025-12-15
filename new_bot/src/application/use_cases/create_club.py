from src.domain.entities.club import Club
from src.domain.entities.club_member import ClubMember
from src.domain.value_objects.ids import ClubId
from src.domain.value_objects.one_time_token import OneTimeToken
from src.domain.enums.club_status import ClubStatus
from ..interfaces.unit_of_work import UnitOfWork
from ..dtos import CreateClubRequest, CreateClubResponse
from ..errors import ConflictError
import uuid

async def execute(uow: UnitOfWork, request: CreateClubRequest) -> CreateClubResponse:
    async with uow:
        # TODO: Check if user exists (Optional, depends on strictness)
        # user = await uow.users.get_by_id(request.user_id)
        
        # Generator for IDs
        club_id = ClubId(uuid.uuid4())
        
        # TODO: Generate real token via Domain Service
        token_value = "generated_token_" + str(uuid.uuid4()) 
        token = OneTimeToken(token_value)

        new_club = Club(
            club_id=club_id,
            tenant_id=request.tenant_id,
            owner_user_id=request.user_id,
            service_id=request.service_id,
            tariff_id=request.tariff_id,
            title=request.title,
            price=request.price,
            status=ClubStatus.RECRUITING
        )

        await uow.clubs.add(new_club)
        
        # TODO: Store token mapping (Club -> Token) if not storing in Club entity directly.
        # This might need a TokenRepository or part of Club attributes if transient.
        # For MVP, assuming Token might be stored in Redis or special table.
        # Placeholder:
        # await uow.tokens.add(token, club_id)

        await uow.commit()

        return CreateClubResponse(club_id=club_id, link_token=token)
