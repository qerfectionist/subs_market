from typing import Optional
from sqlalchemy import String, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid
from ..base import Base
import uuid
from datetime import datetime

class ClubGroupModel(Base):
    __tablename__ = "club_groups"

    club_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("clubs.club_id"), primary_key=True)
    telegram_chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    linked_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    invite_link: Mapped[Optional[str]] = mapped_column(String, nullable=True)
