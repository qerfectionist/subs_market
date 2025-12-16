from sqlalchemy import String, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid
from ..base import Base
from ....domain.enums.club_status import ClubStatus
import uuid

class ClubModel(Base):
    __tablename__ = "clubs"

    club_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    tenant_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=False)
    owner_user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    service_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("subscription_services.service_id"), nullable=False)
    tariff_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("subscription_tariffs.tariff_id"), nullable=False)
    
    title: Mapped[str] = mapped_column(String, nullable=False)
    price_amount: Mapped[int] = mapped_column(Integer, nullable=False) # MoneyKZT -> int
    status: Mapped[ClubStatus] = mapped_column(Enum(ClubStatus), nullable=False)
    short_code: Mapped[str] = mapped_column(String, nullable=True, unique=True)
