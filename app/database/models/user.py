from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Text, ForeignKey, BigInteger
from app.database.base import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.database.models.referal import ReferalSystem


class User(Base):
    __tablename__ = "user"
    _id: Mapped[int] = mapped_column(
        BigInteger, unique=True, primary_key=True, index=True, autoincrement=True
    )
    referer: Mapped[int | None] = mapped_column(ForeignKey(_id))
    email: Mapped[str] = mapped_column(Text, unique=True)
    password: Mapped[str] = mapped_column(Text)

    referal_link: Mapped["ReferalSystem"] = relationship("ReferalSystem", back_populates="owner", cascade="all, delete", lazy='selectin')