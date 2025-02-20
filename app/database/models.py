from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Text, UUID, DateTime, ForeignKey, BigInteger


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    _id = mapped_column(
        BigInteger, unique=True, primary_key=True, index=True, autoincrement=True
    )
    referer = mapped_column(BigInteger, ForeignKey(_id))
    email = mapped_column(Text, unique=True)
    password = mapped_column(Text)


class ReferralSystem(Base):
    __tablename__ = "referal_system"
    _id = mapped_column(UUID, unique=True, primary_key=True)
    owner = mapped_column(Text, ForeignKey(User.email))
    name = mapped_column(Text, unique=True)
    expiration = mapped_column(DateTime)
