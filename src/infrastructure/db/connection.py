from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.infrastructure.config import settings

async_engine = create_async_engine(
    url=settings.db.dsn,
    echo=True,
    pool_pre_ping=True,
)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
