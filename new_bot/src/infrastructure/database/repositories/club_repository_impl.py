from typing import Optional, List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.interfaces.repositories.club_repository import ClubRepository
from src.domain.entities.club import Club
from src.domain.value_objects.ids import ClubId, UserId
from ..models.club import ClubModel
from ..mappers import to_domain_club, to_db_club

class ClubRepositoryImpl(ClubRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, club_id: ClubId) -> Optional[Club]:
        stmt = select(ClubModel).where(ClubModel.club_id == club_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return to_domain_club(model) if model else None

    async def get_by_code(self, code: str) -> Optional[Club]:
        stmt = select(ClubModel).where(ClubModel.short_code == code)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return to_domain_club(model) if model else None

    async def get_all_by_owner(self, owner_id: UserId) -> List[Club]:
        stmt = select(ClubModel).where(ClubModel.owner_user_id == owner_id)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [to_domain_club(model) for model in models]

    async def search(self, category: Optional[str] = None, only_free_slots: bool = False) -> List[Club]:
        stmt = select(ClubModel)
        if category:
            from ..models.subscription_service import SubscriptionServiceModel
            stmt = stmt.join(SubscriptionServiceModel, ClubModel.service_id == SubscriptionServiceModel.service_id)\
                       .where(SubscriptionServiceModel.category == category)
        
        if only_free_slots:
            from sqlalchemy import func
            from ..models.subscription_tariff import SubscriptionTariffModel
            from ..models.club_member import ClubMemberModel
            
            # Subquery to count ACTIVE members
            # Assuming 'ACTIVE' is the status for occupied slots
            member_count_subq = (
                select(func.count(ClubMemberModel.user_id))
                .where(ClubMemberModel.club_id == ClubModel.club_id)
                .where(ClubMemberModel.status.in_(['ACTIVE', 'PENDING'])) # Treat Pending as occupied? Safer.
                .scalar_subquery()
            )
            
            stmt = stmt.join(SubscriptionTariffModel, ClubModel.tariff_id == SubscriptionTariffModel.tariff_id)
            stmt = stmt.where(member_count_subq < SubscriptionTariffModel.capacity)

        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [to_domain_club(model) for model in models]

    async def add(self, club: Club) -> None:
        model = to_db_club(club)
        self._session.add(model)

    async def update(self, club: Club) -> None:
        # Explicit update statement to ensure DB matches domain entity
        stmt = update(ClubModel).where(ClubModel.club_id == club.club_id).values(
            title=club.title,
            price_amount=club.price.amount,
            status=club.status,
            owner_user_id=club.owner_user_id,
            service_id=club.service_id,
            tariff_id=club.tariff_id
        )
        await self._session.execute(stmt)
