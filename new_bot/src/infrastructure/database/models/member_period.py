from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid
from ..base import Base
from ....domain.enums.member_period_status import MemberPeriodStatus
import uuid

class MemberPeriodModel(Base):
    __tablename__ = "member_periods"

    member_period_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    billing_period_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("billing_periods.billing_period_id"), nullable=False, index=True)
    club_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("clubs.club_id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    
    status: Mapped[MemberPeriodStatus] = mapped_column(Enum(MemberPeriodStatus), nullable=False)
