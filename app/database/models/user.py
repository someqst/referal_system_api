from sqlalchemy.orm import mapped_column
from sqlalchemy import Text, ForeignKey, BigInteger
from app.database.base import Base


class User(Base):
    __tablename__ = "user"
    _id = mapped_column(
        BigInteger, unique=True, primary_key=True, index=True, autoincrement=True
    )
    referer = mapped_column(BigInteger, ForeignKey(_id))
    email = mapped_column(Text, unique=True)
    password = mapped_column(Text)