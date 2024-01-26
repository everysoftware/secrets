import asyncio

import pytest
import pytest_asyncio
from alembic.command import upgrade as alembic_upgrade
from httpx import AsyncClient
from starlette.testclient import TestClient

from __main__ import app
from schemes.user import UserRead, UserCreate
from common.settings import cfg
from domain.enums import UserRole
from entities.auth import get_user_create, get_login_data, get_2fa_data
from application.utils import alembic_config_from_url


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    assert cfg.mode == "test"


@pytest.fixture(scope="session")
def alembic_config():
    return alembic_config_from_url(cfg.db.dsn)  # noqa


@pytest.fixture(scope="session", autouse=True)
def run_migrations(alembic_config):
    alembic_upgrade(alembic_config, "head")


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest_asyncio.fixture(scope="session")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="session")
def guest(client: TestClient) -> UserCreate:
    return get_user_create()


@pytest_asyncio.fixture(scope="session")
def user(client: TestClient) -> UserCreate:
    user = get_user_create()

    response = client.post("/auth/register", json=user.model_dump())
    assert response.status_code == 201

    model = UserRead.model_validate(response.json())
    assert model.email == user.email
    assert model.first_name == user.first_name
    assert model.last_name == user.last_name
    assert model.language_code == user.language_code
    assert model.role.value == UserRole.USER.value
    assert model.is_active is True
    assert model.is_superuser is False
    assert model.is_verified is False

    return user


@pytest_asyncio.fixture(scope="session")
def auth_headers(client: TestClient, user: UserCreate) -> dict[str, str]:
    response = client.post("/auth-token/login", data=get_login_data(user))
    assert response.status_code == 200

    json = response.json()
    assert "access_token" in json
    assert json["token_type"] == "bearer"

    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest_asyncio.fixture(scope="session")
def two_fa_headers(
    client: TestClient, user: UserCreate, auth_headers: dict[str, str]
) -> dict[str, str]:
    response = client.post(
        "/auth-token/2fa", json=get_2fa_data(user).model_dump(), headers=auth_headers
    )
    assert response.status_code == 200

    json = response.json()
    assert "access_token" in json
    assert json["token_type"] == "bearer"

    return auth_headers | {"2FA": f"Bearer {response.json()['access_token']}"}
