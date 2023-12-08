# https://github.com/aiogram/aiogram/blob/dev-3.x/tests/conftest.py
import asyncio

import pytest
import pytest_asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from alembic.command import upgrade as alembic_upgrade
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.bot import create_dispatcher
from app.cache import Cache
from core.config import cfg
from app.core import get_async_session_maker, get_async_engine
from utils.alembic import alembic_config_from_url
from utils.mocked_bot import MockedBot
from utils.mocked_db import MockedDatabase
from utils.mocked_redis import MockedRedis


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def bot():
    return MockedBot()


@pytest_asyncio.fixture(scope='session')
async def dispatcher(storage, cache, pool):
    dp = create_dispatcher(storage, cache, pool)
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


@pytest.fixture(scope='session')
def storage():
    return MemoryStorage()


@pytest.fixture(scope='session')
def cache():
    return Cache(redis=MockedRedis())


@pytest.fixture(scope='session')
def engine():
    return get_async_engine(cfg.db.dsl)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_db(engine):
    assert cfg.mode == 'test'


@pytest_asyncio.fixture(scope='session')
async def pool(engine):
    yield get_async_session_maker(engine)


@pytest_asyncio.fixture(scope='session')
async def session(pool: sessionmaker) -> AsyncSession:
    async with pool() as session_:
        yield session_


@pytest_asyncio.fixture(scope='session')
async def db(session: AsyncSession):
    database = MockedDatabase(session)
    yield database
    await database.teardown()


@pytest.fixture(scope='session')
def alembic_config():
    return alembic_config_from_url(cfg.db.dsl)


@pytest.fixture(scope='session', autouse=True)
def run_migrations(alembic_config):
    alembic_upgrade(alembic_config, 'head')
