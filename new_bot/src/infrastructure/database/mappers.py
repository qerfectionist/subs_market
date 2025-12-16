# Pure functions to map between Domain Entities and SQLAlchemy Models
from src.domain.entities.user import User
from src.domain.entities.tenant import Tenant
from src.domain.entities.subscription_service import SubscriptionService
from src.domain.entities.subscription_tariff import SubscriptionTariff
from src.domain.entities.club import Club
from src.domain.entities.club_member import ClubMember
from src.domain.entities.billing_period import BillingPeriod
from src.domain.entities.member_period import MemberPeriod
from src.domain.entities.payment_proof import PaymentProof
from src.domain.entities.dispute import Dispute
from src.domain.entities.dispute_event import DisputeEvent
from src.domain.entities.outbox_event import OutboxEvent

from .models.user import UserModel
from .models.tenant import TenantModel
from .models.subscription_service import SubscriptionServiceModel
from .models.subscription_tariff import SubscriptionTariffModel
from .models.club import ClubModel
from .models.club_member import ClubMemberModel
from .models.billing_period import BillingPeriodModel
from .models.member_period import MemberPeriodModel
from .models.payment_proof import PaymentProofModel
from .models.dispute import DisputeModel
from .models.dispute_event import DisputeEventModel
from .models.outbox_event import OutboxEventModel

from src.domain.value_objects.ids import (
    UserId, TenantId, ClubId, ServiceId, TariffId, BillingPeriodId, 
    MemberPeriodId, PaymentProofId, DisputeId, DisputeEventId, OutboxEventId
)
from src.domain.value_objects.money_kzt import MoneyKZT
from src.domain.value_objects.billing_month import BillingMonth
from src.domain.value_objects.screenshot_hash import ScreenshotHash
from src.domain.enums.club_status import ClubStatus
from src.domain.enums.billing_period_status import BillingPeriodStatus
from src.domain.enums.member_period_status import MemberPeriodStatus

# --- Tenant ---
def to_domain_tenant(model: TenantModel) -> Tenant:
    return Tenant(
        tenant_id=TenantId(model.tenant_id),
        name=model.name
    )

def to_db_tenant(entity: Tenant) -> TenantModel:
    return TenantModel(
        tenant_id=entity.tenant_id,
        name=entity.name
    )

# --- User ---
def to_domain_user(model: UserModel) -> User:
    return User(
        user_id=UserId(model.user_id),
        tenant_id=TenantId(model.tenant_id),
        display_name=model.display_name,
        telegram_user_id=model.telegram_user_id
    )

def to_db_user(entity: User) -> UserModel:
    return UserModel(
        user_id=entity.user_id,
        tenant_id=entity.tenant_id,
        display_name=entity.display_name,
        telegram_user_id=entity.telegram_user_id
    )

# --- Subscription Service ---
def to_domain_service(model: SubscriptionServiceModel) -> SubscriptionService:
    return SubscriptionService(
        service_id=ServiceId(model.service_id),
        tenant_id=TenantId(model.tenant_id),
        name=model.name,
        category=model.category or "OTHER",
        is_active=model.is_active
    )

def to_db_service(entity: SubscriptionService) -> SubscriptionServiceModel:
    return SubscriptionServiceModel(
        service_id=entity.service_id,
        tenant_id=entity.tenant_id,
        name=entity.name,
        category=entity.category,
        is_active=entity.is_active
    )

# --- Subscription Tariff ---
def to_domain_tariff(model: SubscriptionTariffModel) -> SubscriptionTariff:
    return SubscriptionTariff(
        tariff_id=TariffId(model.tariff_id),
        service_id=ServiceId(model.service_id),
        name=model.name,
        capacity=model.capacity,
        currency=model.currency,
        is_active=model.is_active
    )

def to_db_tariff(entity: SubscriptionTariff) -> SubscriptionTariffModel:
    return SubscriptionTariffModel(
        tariff_id=entity.tariff_id,
        service_id=entity.service_id,
        name=entity.name,
        capacity=entity.capacity,
        currency=entity.currency,
        is_active=entity.is_active
    )

# --- Club ---
def to_domain_club(model: ClubModel) -> Club:
    return Club(
        club_id=ClubId(model.club_id),
        tenant_id=TenantId(model.tenant_id),
        owner_user_id=UserId(model.owner_user_id),
        service_id=ServiceId(model.service_id),
        tariff_id=TariffId(model.tariff_id),
        title=model.title,
        price=MoneyKZT(model.price_amount),
        status=model.status,
        short_code=model.short_code
    )

def to_db_club(entity: Club) -> ClubModel:
    return ClubModel(
        club_id=entity.club_id,
        tenant_id=entity.tenant_id,
        owner_user_id=entity.owner_user_id,
        service_id=entity.service_id,
        tariff_id=entity.tariff_id,
        title=entity.title,
        price_amount=entity.price.amount,
        status=entity.status,
        short_code=entity.short_code
    )

# --- Billing Period ---
def to_domain_billing_period(model: BillingPeriodModel) -> BillingPeriod:
    return BillingPeriod(
        billing_period_id=BillingPeriodId(model.billing_period_id),
        club_id=ClubId(model.club_id),
        month=BillingMonth(model.year, model.month),
        status=model.status,
        price=MoneyKZT(model.price_amount)
    )

def to_db_billing_period(entity: BillingPeriod) -> BillingPeriodModel:
    return BillingPeriodModel(
        billing_period_id=entity.billing_period_id,
        club_id=entity.club_id,
        year=entity.month.year,
        month=entity.month.month,
        status=entity.status,
        price_amount=entity.price.amount
    )

# --- Member Period ---
def to_domain_member_period(model: MemberPeriodModel) -> MemberPeriod:
    return MemberPeriod(
        member_period_id=MemberPeriodId(model.member_period_id),
        billing_period_id=BillingPeriodId(model.billing_period_id),
        club_id=ClubId(model.club_id),
        user_id=UserId(model.user_id),
        status=model.status
    )

def to_db_member_period(entity: MemberPeriod) -> MemberPeriodModel:
    return MemberPeriodModel(
        member_period_id=entity.member_period_id,
        billing_period_id=entity.billing_period_id,
        club_id=entity.club_id,
        user_id=entity.user_id,
        status=entity.status
    )

# --- Club Member ---
def to_domain_club_member(model: ClubMemberModel) -> ClubMember:
    return ClubMember(
        club_id=ClubId(model.club_id),
        user_id=UserId(model.user_id),
        joined_at=model.joined_at,
        is_owner=model.is_owner
    )

def to_db_club_member(entity: ClubMember) -> ClubMemberModel:
    return ClubMemberModel(
        club_id=entity.club_id,
        user_id=entity.user_id,
        joined_at=entity.joined_at,
        is_owner=entity.is_owner
    )

# --- Payment Proof ---
def to_domain_payment_proof(model: PaymentProofModel) -> PaymentProof:
    return PaymentProof(
        payment_proof_id=PaymentProofId(model.payment_proof_id),
        billing_period_id=BillingPeriodId(model.billing_period_id),
        club_id=ClubId(model.club_id),
        user_id=UserId(model.user_id),
        screenshot_hash=ScreenshotHash(model.screenshot_hash),
        submitted_at=model.submitted_at
    )

def to_db_payment_proof(entity: PaymentProof) -> PaymentProofModel:
    return PaymentProofModel(
        payment_proof_id=entity.payment_proof_id,
        billing_period_id=entity.billing_period_id,
        club_id=entity.club_id,
        user_id=entity.user_id,
        screenshot_hash=entity.screenshot_hash.value,
        submitted_at=entity.submitted_at
    )

# --- Dispute ---
def to_domain_dispute(model: DisputeModel) -> Dispute:
    return Dispute(
        dispute_id=DisputeId(model.dispute_id),
        club_id=ClubId(model.club_id),
        opened_by_user_id=UserId(model.opened_by_user_id),
        opened_at=model.opened_at,
        status=model.status,
        billing_period_id=BillingPeriodId(model.billing_period_id) if model.billing_period_id else None
    )

def to_db_dispute(entity: Dispute) -> DisputeModel:
    return DisputeModel(
        dispute_id=entity.dispute_id,
        club_id=entity.club_id,
        opened_by_user_id=entity.opened_by_user_id,
        opened_at=entity.opened_at,
        status=entity.status,
        billing_period_id=entity.billing_period_id
    )

# --- Dispute Event ---
def to_domain_dispute_event(model: DisputeEventModel) -> DisputeEvent:
    return DisputeEvent(
        dispute_event_id=DisputeEventId(model.dispute_event_id),
        dispute_id=DisputeId(model.dispute_id),
        actor_user_id=UserId(model.actor_user_id),
        type=model.type,
        payload=model.payload,
        created_at=model.created_at
    )

def to_db_dispute_event(entity: DisputeEvent) -> DisputeEventModel:
    return DisputeEventModel(
        dispute_event_id=entity.dispute_event_id,
        dispute_id=entity.dispute_id,
        actor_user_id=entity.actor_user_id,
        type=entity.type,
        payload=entity.payload,
        created_at=entity.created_at
    )

# --- Outbox Event ---
def to_domain_outbox_event(model: OutboxEventModel) -> OutboxEvent:
    return OutboxEvent(
        outbox_event_id=OutboxEventId(model.outbox_event_id),
        aggregate_type=model.aggregate_type,
        aggregate_id=model.aggregate_id,
        event_type=model.event_type,
        payload=model.payload,
        occurred_at=model.occurred_at,
        published_at=model.published_at
    )

def to_db_outbox_event(entity: OutboxEvent) -> OutboxEventModel:
    return OutboxEventModel(
        outbox_event_id=entity.outbox_event_id,
        aggregate_type=entity.aggregate_type,
        aggregate_id=entity.aggregate_id,
        event_type=entity.event_type,
        payload=entity.payload,
        occurred_at=entity.occurred_at,
        published_at=entity.published_at
    )
