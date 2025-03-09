from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import UUID, DateTime, ForeignKey, String
from app.database.base import Base
from app.database.models.user import User
from datetime import datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.database.models.referal import User


class ReferalSystem(Base):
    __tablename__ = "referal_system"
    _id: Mapped[UUID] = mapped_column(UUID, unique=True, primary_key=True, index=True)
    owner_email: Mapped[str] = mapped_column(ForeignKey("user.email"))
    code: Mapped[str] = mapped_column(String, unique=True)
    expiration: Mapped[datetime] = mapped_column(DateTime)

    owner: Mapped["User"] = relationship("User", back_populates="referal_link", lazy='selectin')
