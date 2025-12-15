from typing import Protocol
from .repositories.user_repository import UserRepository
from .repositories.club_repository import ClubRepository
from .repositories.billing_period_repository import BillingPeriodRepository
from .repositories.membership_repository import MembershipRepository
from .repositories.payment_proof_repository import PaymentProofRepository
from .repositories.dispute_repository import DisputeRepository
from .repositories.outbox_repository import OutboxRepository

class UnitOfWork(Protocol):
    users: UserRepository
    clubs: ClubRepository
    billing_periods: BillingPeriodRepository
    memberships: MembershipRepository
    payment_proofs: PaymentProofRepository
    disputes: DisputeRepository
    outbox: OutboxRepository

    async def aenter(self) -> "UnitOfWork":
        ...

    async def aexit(self, exc_type, exc, tb) -> None:
        ...

    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...
