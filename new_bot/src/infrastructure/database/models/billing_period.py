from sqlalchemy import Integer, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid
from ..base import Base
from ....domain.enums.billing_period_status import BillingPeriodStatus
import uuid

class BillingPeriodModel(Base):
    __tablename__ = "billing_periods"

    billing_period_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    club_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("clubs.club_id"), nullable=False, index=True)
    
    # BillingMonth mapping
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    
    status: Mapped[BillingPeriodStatus] = mapped_column(Enum(BillingPeriodStatus), nullable=False)
    price_amount: Mapped[int] = mapped_column(Integer, nullable=False) # MoneyKZT

    __table_args__ = (
        UniqueConstraint('club_id', 'year', 'month', name='uq_billing_period_club_month'),
    )
