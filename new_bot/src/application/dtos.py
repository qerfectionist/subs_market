from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from src.domain.value_objects.ids import (
    UserId, ClubId, TenantId, ServiceId, TariffId, 
    PaymentProofId, DisputeId, DisputeEventId, MemberPeriodId,
    BillingPeriodId
)
from src.domain.value_objects.money_kzt import MoneyKZT
from src.domain.value_objects.one_time_token import OneTimeToken
from src.domain.value_objects.screenshot_hash import ScreenshotHash
from src.domain.enums.club_status import ClubStatus
from src.domain.enums.billing_period_status import BillingPeriodStatus
from src.domain.enums.member_period_status import MemberPeriodStatus
from src.domain.entities.club import Club

# Ensure User (Identity Mapping)
@dataclass(frozen=True)
class EnsureUserRequest:
    tenant_id: TenantId
    telegram_user_id: int
    display_name: str

@dataclass(frozen=True)
class EnsureUserResponse:
    user_id: UserId
    is_new: bool

# Create Club
@dataclass(frozen=True)
class CreateClubRequest:
    user_id: UserId
    tenant_id: TenantId
    service_id: ServiceId
    tariff_id: TariffId
    title: str
    price: MoneyKZT

@dataclass(frozen=True)
class CreateClubResponse:
    club_id: ClubId
    link_token: OneTimeToken
    short_code: str | None = None

# Link Group
@dataclass(frozen=True)
class LinkGroupRequest:
    user_id: UserId
    chat_id: int
    token: OneTimeToken
    invite_link: Optional[str] = None

@dataclass(frozen=True)
class LinkGroupResponse:
    club_id: ClubId
    success: bool

# Join Club
@dataclass(frozen=True)
class JoinClubRequest:
    user_id: UserId
    club_id: ClubId

@dataclass(frozen=True)
class JoinClubResponse:
    success: bool
    status: str # e.g. "pending_approval"

# Approve Member
@dataclass(frozen=True)
class ApproveMemberRequest:
    owner_id: UserId
    club_id: ClubId
    member_user_id: UserId
    approved: bool

@dataclass(frozen=True)
class ApproveMemberResponse:
    success: bool

# Open Billing Period
@dataclass(frozen=True)
class OpenBillingPeriodRequest:
    club_id: ClubId
    actor_user_id: UserId # Owner or System

@dataclass(frozen=True)
class OpenBillingPeriodResponse:
    billing_period_id: BillingPeriodId
    status: BillingPeriodStatus

# Submit Payment Proof
@dataclass(frozen=True)
class SubmitPaymentProofRequest:
    user_id: UserId
    club_id: ClubId
    file_id: str # Telegram File ID
    screenshot_hash: ScreenshotHash

@dataclass(frozen=True)
class SubmitPaymentProofResponse:
    payment_proof_id: PaymentProofId
    member_period_status: MemberPeriodStatus

# Confirm Payment
@dataclass(frozen=True)
class ConfirmPaymentRequest:
    owner_id: UserId
    payment_proof_id: PaymentProofId
    approved: bool

@dataclass(frozen=True)
class ConfirmPaymentResponse:
    member_period_id: MemberPeriodId
    new_status: MemberPeriodStatus

# Mark Overdue
@dataclass(frozen=True)
class MarkOverdueRequest:
    club_id: ClubId # or run for all? Usually per club or per period.
    billing_period_id: BillingPeriodId

@dataclass(frozen=True)
class MarkOverdueResponse:
    overdue_count: int

# Remove Member
@dataclass(frozen=True)
class RemoveMemberRequest:
    owner_id: UserId
    club_id: ClubId
    target_user_id: UserId
    reason: str

@dataclass(frozen=True)
class RemoveMemberResponse:
    success: bool

# Raise Dispute
@dataclass(frozen=True)
class RaiseDisputeRequest:
    user_id: UserId
    club_id: ClubId
    reason: str

@dataclass(frozen=True)
class RaiseDisputeResponse:
    dispute_id: DisputeId

# Resolve Dispute
@dataclass(frozen=True)
class ResolveDisputeRequest:
    admin_id: UserId # System Admin? or Club Owner? Assuming Support/System or Auto
    dispute_id: DisputeId
    resolution: str
    status: str

@dataclass(frozen=True)
class ResolveDisputeResponse:
    success: bool

# Get User Clubs
@dataclass(frozen=True)
class GetUserClubsRequest:
    user_id: UserId

@dataclass(frozen=True)
class GetUserClubsResponse:
    clubs: List[Club] # Note: Club needs to be imported or use ForwardRef/Any if circular. DataClasses usually fine if imported.
    # Current file imports src.domain.entities.club? No. 
    # I need to check imports at top. dtos.py imports value objects but not Entities usually?
    # Checking lines 1-15: No Club Entity import.
    # I need to add `from src.domain.entities.club import Club` to dtos.py 
    # BUT Entities might import Value Objects, so circular import risk is low.
    # I'll enable generic imports.

# Search Clubs
@dataclass(frozen=True)
class SearchClubsRequest:
    category: Optional[str] = None
    only_free_slots: bool = False

@dataclass(frozen=True)
class SearchClubsResponse:
    clubs: List['Club'] # usage of string forward ref if Club not available

# Get Club Details
@dataclass(frozen=True)
class GetClubDetailsRequest:
    club_id: ClubId

@dataclass(frozen=True)
class GetClubDetailsResponse:
    club: 'Club'
    member_count: int
    tariff_capacity: int
