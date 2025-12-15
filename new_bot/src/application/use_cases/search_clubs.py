from dataclasses import dataclass
from typing import List, Optional
from src.application.interfaces.unit_of_work import UnitOfWork
from src.domain.entities.club import Club
from src.application.dtos import SearchClubsRequest, SearchClubsResponse

async def execute(uow: UnitOfWork, request: SearchClubsRequest) -> SearchClubsResponse:
    async with uow:
        # For now, we might need a search method in repo.
        # Or simple: fetch all and filter (MVP). 
        # But `SubscriptionService` info is needed (Join).
        # We need a query that joins Club -> Service.
        
        # Better: add `search` to repository.
        # For step simplicity, assuming `search_clubs` exists in repo.
        clubs = await uow.clubs.search(category=request.category)
        return SearchClubsResponse(clubs=clubs)
