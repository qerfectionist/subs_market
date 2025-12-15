from enum import Enum

class MemberPeriodStatus(str, Enum):
    PENDING_PAYMENT = "pending_payment"
    PROOF_SUBMITTED = "proof_submitted"
    CONFIRMED = "confirmed"
    OVERDUE = "overdue"
    REMOVED = "removed"
