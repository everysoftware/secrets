# https://github.com/aiogram/aiogram/blob/dev-3.x/tests/conftest.py
import asyncio

import pytest
import pytest_asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from alembic.command import upgrade as alembic_upgrade
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from config import cfg
from db import get_session_maker, create_async_engine
from dispatcher import create_dispatcher
from utils.alembic import alembic_config_from_url
from utils.mocked_bot import MockedBot
from utils.mocked_db import MockedDatabase


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    asyncio.set_event_loop(loop)


@pytest.fixture(scope='session')
def bot():
    return MockedBot()


@pytest_asyncio.fixture(scope='session')
async def dispatcher(storage):
    dp = create_dispatcher(storage)
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


@pytest.fixture(scope='session')
def storage():
    return MemoryStorage()


@pytest.fixture(scope='session')
def engine():
    return create_async_engine(cfg.db.build_connection_str())


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_db(engine):
    assert cfg.mode == 'test'


@pytest_asyncio.fixture(scope='session')
async def pool(engine):
    yield get_session_maker(engine)


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
    return alembic_config_from_url(cfg.db.build_connection_str())


@pytest.fixture(scope='session', autouse=True)
def run_migrations(alembic_config):
    alembic_upgrade(alembic_config, 'head')
