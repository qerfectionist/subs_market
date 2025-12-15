from src.domain.services.market_engine import payment_proof_service
from ..interfaces.unit_of_work import UnitOfWork
from ..dtos import SubmitPaymentProofRequest, SubmitPaymentProofResponse
from ..errors import NotFoundError, ConflictError
from src.domain.entities.payment_proof import PaymentProof
from src.domain.value_objects.ids import PaymentProofId
from src.domain.value_objects.screenshot_hash import ScreenshotHash
from src.domain.enums.member_period_status import MemberPeriodStatus

async def execute(uow: UnitOfWork, request: SubmitPaymentProofRequest) -> SubmitPaymentProofResponse:
    async with uow:
        # 1. Resolve active billing period
        # We assume proof is for the current *latest* open period.
        # If the user wants to pay for a past period, that's a more complex flow not handled here yet.
        period = await uow.billing_periods.get_latest_period(request.club_id)
        
        if not period or period.status != BillingPeriodStatus.OPEN:
             # Can't submit proof if no period is open
             raise NotFoundError("No open billing period found for this club")
        
        # 2. Find Member Period
        mp = await uow.memberships.get_by_period_and_user(period.billing_period_id, request.user_id)
        if not mp:
             raise NotFoundError("User is not a member in this billing period")

        # 3. Deduplicate Hash
        is_dupe = await uow.payment_proofs.exists_hash_for_period(
            billing_period_id=period.billing_period_id,
            screenshot_hash=request.screenshot_hash
        )
        if is_dupe:
            raise ConflictError("Duplicate screenshot detected. Please do not re-upload the same receipt.")

        # 4. Create Proof Entity
        from datetime import datetime
        import uuid
        
        # Determine current UTC time. Ideally use an injected clock service, but datetime.utcnow() is fine for MVP.
        # Only issue is timezone awareness, typically better to use datetime.now(timezone.utc)
        from datetime import timezone
        now_utc = datetime.now(timezone.utc)

        proof_id = uuid.uuid4()
        proof = PaymentProof(
             payment_proof_id=proof_id,
             billing_period_id=period.billing_period_id,
             club_id=request.club_id,
             user_id=request.user_id,
             screenshot_hash=request.screenshot_hash,
             submitted_at=now_utc
        )
        await uow.payment_proofs.add(proof)

        # 5. Update Member State -> PROOF_SUBMITTED
        # Only update if PENDING. If CONFIRMED, we shouldn't allow (or maybe allow as re-submission?)
        # For now, allow re-submission if not CONFIRMED.
        if mp.status != MemberPeriodStatus.CONFIRMED:
             # We need to recreate the entity with new status because it's frozen
             # Using dataclasses.replace
             from dataclasses import replace
             mp_updated = replace(mp, status=MemberPeriodStatus.PROOF_SUBMITTED)
             await uow.memberships.update_member_period(mp_updated)
             final_status = MemberPeriodStatus.PROOF_SUBMITTED
        else:
             final_status = MemberPeriodStatus.CONFIRMED # Already confirmed ignore update

        await uow.commit()
        return SubmitPaymentProofResponse(
            payment_proof_id=proof_id, 
            member_period_status=final_status
        )
