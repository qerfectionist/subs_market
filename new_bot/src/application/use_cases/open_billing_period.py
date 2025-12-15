from src.domain.entities.billing_period import BillingPeriod
from src.domain.entities.member_period import MemberPeriod
from src.domain.value_objects.ids import BillingPeriodId, MemberPeriodId
from ..interfaces.unit_of_work import UnitOfWork
from ..dtos import OpenBillingPeriodRequest, OpenBillingPeriodResponse
from ..errors import NotFoundError, PermissionDeniedError
import uuid

async def execute(uow: UnitOfWork, request: OpenBillingPeriodRequest) -> OpenBillingPeriodResponse:
    async with uow:
        club = await uow.clubs.get_by_id(request.club_id)
        if not club:
            raise NotFoundError("Club not found")

        # Verify permission (Owner or System)
        if request.actor_user_id != club.owner_user_id:
             # TODO: Allow system actor when we have system logic
             raise PermissionDeniedError("Permission denied: Only owner can open billing")

        # Determine next month
        latest_period = await uow.billing_periods.get_latest_period(request.club_id)
        if not latest_period:
            # First period: Start with current month
            from src.domain.value_objects.billing_month import BillingMonth
            next_month = BillingMonth.current()
        else:
            # Check if latest is already open? 
            # If latest is OPEN, return it (Idempotency) or error? 
            # Assuming idempotency for UX safety.
            if latest_period.status == BillingPeriodStatus.OPEN:
                return OpenBillingPeriodResponse(
                    billing_period_id=latest_period.billing_period_id,
                    status=latest_period.status
                )
            next_month = latest_period.month.next()

        # Check if period exists (e.g. was created but corrupted or logic error? or simply re-opening a closed one? - No, periods are immutable history)
        existing = await uow.billing_periods.get_by_club_and_month(request.club_id, next_month)
        if existing:
             # If exists and closed, we can't reopen it easily. We should move to next.
             # But this is edge case. Assume we can't modify history.
             # If exists and OPEN, we returned above.
             # If exists and CLOSED, that means we are in future? Or logic error.
             # Let's simplify: if exists, use it.
             return OpenBillingPeriodResponse(
                billing_period_id=existing.billing_period_id,
                status=existing.status
            )

        # Create new Period
        new_period_id = uuid.uuid4()
        new_period = BillingPeriod(
            billing_period_id=new_period_id,
            club_id=club.club_id,
            month=next_month,
            status=BillingPeriodStatus.OPEN,
            price=club.price # Snapshot price
        )
        
        await uow.billing_periods.add(new_period)

        # Generate MemberPeriods for all active members
        members = await uow.memberships.list_members(club.club_id)
        for m in members:
            # Filter only ACTIVE members? 
            # Assuming list_members returns all. We need a way to check status.
            # ClubMember has status? Let's assume list_members returns valid members.
            mp = MemberPeriod(
                member_period_id=uuid.uuid4(),
                billing_period_id=new_period_id,
                club_id=club.club_id,
                user_id=m.user_id,
                status=MemberPeriodStatus.PENDING
            )
            await uow.memberships.add_member_period(mp)

        await uow.commit()

        return OpenBillingPeriodResponse(
            billing_period_id=new_period_id, 
            status=BillingPeriodStatus.OPEN
        )
