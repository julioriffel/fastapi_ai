from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)


async def init_db() -> None:
    async with engine.begin():
        # await conn.run_sync(SQLModel.metadata.drop_all)
        # await conn.run_sync(SQLModel.metadata.create_all)
        pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,  # type: ignore[call-overload]
    )
    async with async_session() as session:
        yield session
