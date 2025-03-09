from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.user import User
from app.database.models.referal import ReferalSystem


class UserRepository:
    @classmethod
    async def create(
        cls, email: str, encrypted_password: str, referal_code: str | None, session: AsyncSession
    ):
        referer = None
        if referal_code:
            referal_system = (
                await session.execute(
                    select(ReferalSystem).where(ReferalSystem.code == referal_code)
                )).scalar_one_or_none()
            referer = referal_system.owner._id

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
                .join(ReferalSystem, User.email == ReferalSystem.owner_email)
                .where(ReferalSystem.code == referal_word)
            )
        ).scalar_one_or_none()
    
    
user_repository = UserRepository()
