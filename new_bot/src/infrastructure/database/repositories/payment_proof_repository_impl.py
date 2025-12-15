from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.interfaces.repositories.payment_proof_repository import PaymentProofRepository
from src.domain.entities.payment_proof import PaymentProof
from src.domain.value_objects.ids import PaymentProofId, BillingPeriodId
from ....domain.value_objects.screenshot_hash import ScreenshotHash
from ..models.payment_proof import PaymentProofModel
from ..mappers import to_domain_payment_proof, to_db_payment_proof

class PaymentProofRepositoryImpl(PaymentProofRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, payment_proof_id: PaymentProofId) -> Optional[PaymentProof]:
        stmt = select(PaymentProofModel).where(PaymentProofModel.payment_proof_id == payment_proof_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return to_domain_payment_proof(model) if model else None

    async def exists_hash_for_period(self, billing_period_id: BillingPeriodId, screenshot_hash: ScreenshotHash) -> bool:
        stmt = select(PaymentProofModel).where(
            PaymentProofModel.billing_period_id == billing_period_id,
            PaymentProofModel.screenshot_hash == screenshot_hash.value
        )
        result = await self._session.execute(stmt)
        return result.first() is not None

    async def add(self, proof: PaymentProof) -> None:
        model = to_db_payment_proof(proof)
        self._session.add(model)
