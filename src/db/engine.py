from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as create_async_engine_
from sqlalchemy.orm import sessionmaker

from src.config import cfg


def create_async_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine_(url=url,
                                echo=cfg.debug,
                                pool_pre_ping=True)


def get_session_maker(engine: AsyncEngine = None) -> sessionmaker:
    return sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )


@DeprecationWarning
async def proceed_schemes(*_) -> None:
    pass
