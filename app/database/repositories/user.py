from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.user import User
from app.database.models.referal import ReferralSystem


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
    
    
user_repository = UserRepository()
