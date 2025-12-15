from ..interfaces.unit_of_work import UnitOfWork
from ..dtos import ConfirmPaymentRequest, ConfirmPaymentResponse
from ..errors import NotFoundError, PermissionDeniedError
from src.domain.enums.member_period_status import MemberPeriodStatus

async def execute(uow: UnitOfWork, request: ConfirmPaymentRequest) -> ConfirmPaymentResponse:
    async with uow:
        # 1. Load Proof
        proof = await uow.payment_proofs.get_by_id(request.payment_proof_id)
        if not proof:
            raise NotFoundError("Proof not found")

        # 2. Verify Owner
        club = await uow.clubs.get_by_id(proof.club_id)
        if not club:
             raise NotFoundError("Club not found")
        
        if club.owner_user_id != request.owner_id:
            raise PermissionDeniedError("Permission denied: Not the club owner")
            
        # 3. Retrieve Member Period
        # We need the member period associated with this payment proof (same billing period and user)
        mp = await uow.memberships.get_by_period_and_user(proof.billing_period_id, proof.user_id)
        if not mp:
             raise NotFoundError("Member period not found for this proof")

        # 4. Update Status
        if request.approved:
            new_status = MemberPeriodStatus.CONFIRMED
        else:
            new_status = MemberPeriodStatus.PENDING_PAYMENT # Rejected, user must pay/upload again
        
        # We need to recreate the entity with new status because it's frozen
        from dataclasses import replace
        mp_updated = replace(mp, status=new_status)
        await uow.memberships.update_member_period(mp_updated)

        await uow.commit()
        return ConfirmPaymentResponse(member_period_id=mp.member_period_id, new_status=new_status)
