from dataclasses import dataclass
from datetime import datetime
from ..value_objects.ids import PaymentProofId, BillingPeriodId, ClubId, UserId
from ..value_objects.screenshot_hash import ScreenshotHash

@dataclass(frozen=True)
class PaymentProof:
    payment_proof_id: PaymentProofId
    billing_period_id: BillingPeriodId
    club_id: ClubId
    user_id: UserId
    screenshot_hash: ScreenshotHash
    submitted_at: datetime
