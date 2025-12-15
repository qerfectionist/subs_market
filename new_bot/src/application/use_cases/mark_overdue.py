from ..interfaces.unit_of_work import UnitOfWork
from ..dtos import MarkOverdueRequest, MarkOverdueResponse

async def execute(uow: UnitOfWork, request: MarkOverdueRequest) -> MarkOverdueResponse:
    async with uow:
        # 1. Load Period
        # period = ...

        # 2. Find Pending Payments past deadline
        # pending = ...

        # 3. Update to OVERDUE
        count = 0
        # for mp in pending:
        #    mp.status = MemberPeriodStatus.OVERDUE
        #    await uow.memberships.update_member_period(mp)
        #    count += 1
        
        await uow.commit()
        return MarkOverdueResponse(overdue_count=count)
