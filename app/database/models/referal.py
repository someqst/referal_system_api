from sqlalchemy.orm import mapped_column
from sqlalchemy import Text, UUID, DateTime, ForeignKey
from app.database.base import Base


class ReferralSystem(Base):
    __tablename__ = "referal_system"
    _id = mapped_column(UUID, unique=True, primary_key=True)
    owner = mapped_column(Text, ForeignKey("user.email"))
    name = mapped_column(Text, unique=True)
    expiration = mapped_column(DateTime)