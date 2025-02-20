from uuid import uuid4
from sqlalchemy import select, insert
from app.database.models import User, ReferralSystem
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    @classmethod
    async def create(
        cls, email, encrypted_password, referal_code, session: AsyncSession
    ):
        referer = None
        if referal_code:
            referer = (
                await session.execute(
                    select(User._id)
                    .join(ReferralSystem, User.email == ReferralSystem.owner)
                    .where(ReferralSystem.name == referal_code)
                )
            ).scalar_one_or_none()

        await session.execute(
            insert(User).values(
                email=email, password=encrypted_password, referer=referer
            )
        )
        await session.commit()

    @classmethod
    async def get_by_email(cls, email, session: AsyncSession) -> User | None:
        return (
            await session.execute(select(User).where(User.email == email))
        ).scalar_one_or_none()

    @classmethod
    async def get_by_referal_word(
        cls, referal_word, session: AsyncSession
    ) -> User | None:
        return (
            await session.execute(
                select(User)
                .join(ReferralSystem, User.email == ReferralSystem.owner)
                .where(ReferralSystem.name == referal_word)
            )
        ).scalar_one_or_none()


class ReferalRepository:
    @classmethod
    async def create(cls, name, owner, expiration, session: AsyncSession):
        await session.execute(
            insert(ReferralSystem).values(
                _id=str(uuid4()), owner=owner, name=name, expiration=expiration
            )
        )
        await session.commit()

    @classmethod
    async def get_code(cls, name, session: AsyncSession):
        return (
            await session.execute(
                select(ReferralSystem).where(ReferralSystem.name == name)
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
                select(ReferralSystem.name).where(ReferralSystem.owner == email)
            )
        ).scalar_one_or_none()


user_repository = UserRepository()
referal_repository = ReferalRepository()
