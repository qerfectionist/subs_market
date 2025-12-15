from typing import Protocol, Optional
from src.domain.entities.payment_proof import PaymentProof
from src.domain.value_objects.ids import PaymentProofId, BillingPeriodId
from src.domain.value_objects.screenshot_hash import ScreenshotHash

class PaymentProofRepository(Protocol):
    async def get_by_id(self, payment_proof_id: PaymentProofId) -> Optional[PaymentProof]:
        ...

    async def exists_hash_for_period(self, billing_period_id: BillingPeriodId, screenshot_hash: ScreenshotHash) -> bool:
        ...

    async def add(self, proof: PaymentProof) -> None:
        ...
