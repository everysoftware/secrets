# Reference:
# https://github.com/aiogram/aiogram/blob/dev-3.x/tests/conftest.py
import asyncio

import pytest
import pytest_asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from alembic.command import upgrade as alembic_upgrade
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.api.app import app
# from app.bot.dispatcher import create_dispatcher
from app.cache import Cache
from app.core import get_async_session_maker, get_async_engine
from app.core.config import cfg
from utils.alembic import alembic_config_from_url
from utils.entities import TEST_USER_LOGIN, TEST_USER_2FA
from utils.mocked_bot import MockedBot
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
    # dp = create_dispatcher(storage, cache, pool)
    dp = Dispatcher()
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
    return get_async_engine(cfg.db.dsl)  # noqa


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_db(engine):
    assert cfg.mode == 'test'


@pytest_asyncio.fixture(scope='session')
async def pool(engine):
    yield get_async_session_maker(engine)


@pytest_asyncio.fixture(scope='session')
async def session(pool: sessionmaker):
    async with pool() as session_:
        yield session_


@pytest_asyncio.fixture(scope='session')
async def db(session: AsyncSession):
    database = MockedDatabase(session)
    yield database
    await database.teardown()


@pytest.fixture(scope='session')
def alembic_config():
    return alembic_config_from_url(cfg.db.dsl)  # noqa


@pytest.fixture(scope='session', autouse=True)
def run_migrations(alembic_config):
    alembic_upgrade(alembic_config, 'head')


@pytest.fixture(scope='session')
def client():
    return TestClient(app)


@pytest_asyncio.fixture(scope='session')
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope='session')
def auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post("/auth-token/login", data=TEST_USER_LOGIN)
    assert response.status_code == 200

    json = response.json()
    assert "access_token" in json
    assert json["token_type"] == "bearer"

    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest_asyncio.fixture(scope='session')
def two_fa_headers(client: TestClient, auth_headers: dict[str, str]) -> dict[str, str]:
    response = client.post("/auth-token/2fa", json=TEST_USER_2FA.model_dump(), headers=auth_headers)
    assert response.status_code == 200

    json = response.json()
    assert "access_token" in json
    assert json["token_type"] == "bearer"

    return auth_headers | {"2FA": f"Bearer {response.json()['access_token']}"}
