from typing import AsyncGenerator

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker)
from sqlalchemy.ext.asyncio import create_async_engine as create_async_engine_

from app.core.config import cfg


def get_async_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine_(url=url, echo=cfg.debug, pool_pre_ping=True)


def get_async_session_maker(engine: AsyncEngine | None = None) -> async_sessionmaker:
    return async_sessionmaker(
        engine or get_async_engine(cfg.db.dsl),
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def async_session_factory() -> AsyncGenerator[AsyncSession, None]:
    maker = get_async_session_maker()
    async with maker() as session:
        yield session
