from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from ...application.interfaces.unit_of_work import UnitOfWork
from .repositories.user_repository_impl import UserRepositoryImpl
from .repositories.club_repository_impl import ClubRepositoryImpl
from .repositories.billing_period_repository_impl import BillingPeriodRepositoryImpl
from .repositories.membership_repository_impl import MembershipRepositoryImpl
from .repositories.payment_proof_repository_impl import PaymentProofRepositoryImpl
from .repositories.dispute_repository_impl import DisputeRepositoryImpl
from .repositories.outbox_repository_impl import OutboxRepositoryImpl

class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> UnitOfWork:
        self._session = self._session_factory()
        self.users = UserRepositoryImpl(self._session)
        self.clubs = ClubRepositoryImpl(self._session)
        self.billing_periods = BillingPeriodRepositoryImpl(self._session)
        self.memberships = MembershipRepositoryImpl(self._session)
        self.payment_proofs = PaymentProofRepositoryImpl(self._session)
        self.disputes = DisputeRepositoryImpl(self._session)
        self.outbox = OutboxRepositoryImpl(self._session)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._session:
            if exc_type:
                await self._session.rollback()
            await self._session.close()

    async def commit(self) -> None:
        if self._session:
            await self._session.commit()

    async def rollback(self) -> None:
        if self._session:
            await self._session.rollback()
