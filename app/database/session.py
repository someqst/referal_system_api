from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core.config import settings


engine = create_async_engine(settings.DB_URI.get_secret_value())
LocalSession = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db():
    async with LocalSession() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()