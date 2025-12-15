from dataclasses import dataclass
from ..value_objects.ids import BillingPeriodId, ClubId
from ..value_objects.billing_month import BillingMonth
from ..value_objects.money_kzt import MoneyKZT
from ..enums.billing_period_status import BillingPeriodStatus

@dataclass(frozen=True)
class BillingPeriod:
    billing_period_id: BillingPeriodId
    club_id: ClubId
    month: BillingMonth
    status: BillingPeriodStatus
    price: MoneyKZT
