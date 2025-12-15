from typing import NewType
from uuid import UUID

TenantId = NewType("TenantId", UUID)
UserId = NewType("UserId", UUID)
ClubId = NewType("ClubId", UUID)
BillingPeriodId = NewType("BillingPeriodId", UUID)
MemberPeriodId = NewType("MemberPeriodId", UUID)
PaymentProofId = NewType("PaymentProofId", UUID)
DisputeId = NewType("DisputeId", UUID)
DisputeEventId = NewType("DisputeEventId", UUID)
RiskFlagId = NewType("RiskFlagId", UUID)
OutboxEventId = NewType("OutboxEventId", UUID)
ServiceId = NewType("ServiceId", UUID)
TariffId = NewType("TariffId", UUID)
