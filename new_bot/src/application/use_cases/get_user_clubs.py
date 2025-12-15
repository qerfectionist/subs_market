from dataclasses import dataclass
from typing import List
from src.application.interfaces.unit_of_work import UnitOfWork
from src.domain.entities.club import Club
from src.domain.value_objects.ids import UserId
from src.application.dtos import GetUserClubsRequest, GetUserClubsResponse

async def execute(uow: UnitOfWork, request: GetUserClubsRequest) -> GetUserClubsResponse:
    async with uow:
        clubs = await uow.clubs.get_all_by_owner(request.user_id)
        return GetUserClubsResponse(clubs=clubs)
