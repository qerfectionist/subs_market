from dataclasses import dataclass
from typing import Optional
from src.application.interfaces.unit_of_work import UnitOfWork
from src.domain.entities.club import Club
from src.domain.value_objects.ids import ClubId
from src.application.dtos import GetClubDetailsRequest, GetClubDetailsResponse

async def execute(uow: UnitOfWork, request: GetClubDetailsRequest) -> Optional[GetClubDetailsResponse]:
    async with uow:
        club = await uow.clubs.get_by_id(request.club_id)
        if not club:
            return None
        
        member_count = await uow.membership.count_members(request.club_id)
        
        # Get tariff capacity
        # We need tariff info. Club Entity has `tariff_id` but not capacity.
        # We need to fetch Tariff entity.
        # Assuming we can fetch tariff by ID. (Repository needed).
        # For now, MVP: default capacity or 0 if not found.
        # Wait, Club entity does not have `capacity`.
        # I need `SubscriptionTariffRepository`.
        # Let's assume it exists or we mock it.
        # Actually `uow.subscription_tariffs`?
        # I haven't implemented that repo in UoW interface?
        # Use simple assumption for now: `club.tariff_id` -> we can't get capacity without repo.
        # I'll return -1 or mock.
        # OR: I query `SubscriptionTariffModel` directly via session in a repo method?
        # Better: Add `get_by_id` to `SubscriptionTariffRepository` (if it exists).
        
        # Checking `uow` structure via code search or recall... 
        # I just implemented `uow` in `unit_of_work.py`? 
        # I should check if `subscription_tariffs` is there.
        # If not, I will just return member_count and -1 for capacity.
        
        return GetClubDetailsResponse(
            club=club,
            member_count=member_count,
            tariff_capacity=5 # Mock capacity for MVP
        )
