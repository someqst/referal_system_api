from uuid import uuid4
from sqlalchemy import select, insert
from app.database.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.referal import ReferalSystem


class ReferalRepository:
    @classmethod
    async def create(cls, code, owner_email, expiration, session: AsyncSession):
        await session.execute(
            insert(ReferalSystem).values(
                _id=str(uuid4()), owner_email=owner_email, code=code, expiration=expiration
            )
        )
        await session.commit()

    @classmethod
    async def get_code(cls, code, session: AsyncSession):
        return (
            await session.execute(
                select(ReferalSystem).where(ReferalSystem.code == code)
            )
        ).scalar_one_or_none()

    # Тут в целях безопасности не отдаю password
    @classmethod
    async def get_all_referals(cls, referrer_id, session: AsyncSession):
        return (
            (
                await session.execute(
                    select(User._id, User.email).where(User.referer == referrer_id)
                )
            )
            .mappings()
            .all()
        )

    @classmethod
    async def get_by_email(cls, email, session: AsyncSession):
        return (
            await session.execute(
                select(ReferalSystem.code).where(ReferalSystem.owner_email == email)
            )
        ).scalar_one_or_none()
    

referal_repository = ReferalRepository()
