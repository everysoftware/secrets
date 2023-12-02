from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker)
from sqlalchemy.ext.asyncio import create_async_engine as create_async_engine_

from src.config import cfg


def create_async_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine_(url=url, echo=cfg.debug, pool_pre_ping=True)


def async_session_factory(engine: AsyncEngine | None = None) -> async_sessionmaker:
    return async_sessionmaker(
        engine or create_async_engine(cfg.db.build_connection_str()),
        class_=AsyncSession,
        expire_on_commit=False,
    )
