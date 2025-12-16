from typing import Protocol, Optional, List
from src.domain.entities.club import Club
from src.domain.value_objects.ids import ClubId, UserId

class ClubRepository(Protocol):
    async def get_by_id(self, club_id: ClubId) -> Optional[Club]:
        ...

    async def get_by_code(self, code: str) -> Optional[Club]:
        ...

    async def get_all_by_owner(self, owner_id: UserId) -> List[Club]:
        ...

    async def search(self, category: Optional[str] = None) -> List[Club]:
        ...

    async def add(self, club: Club) -> None:
        ...

    async def update(self, club: Club) -> None:
        ...
