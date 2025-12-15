from enum import Enum

class BillingPeriodStatus(str, Enum):
    PLANNED = "planned"
    OPEN = "open"
    CLOSING = "closing"
    CLOSED = "closed"
