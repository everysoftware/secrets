from starlette.testclient import TestClient

from api.auth.schemes import UserRead
from core.enums import UserRole
from utils.entities import TEST_USER_CREATE, TEST_USER_LOGIN, TEST_USER_2FA


def test_register(client: TestClient):
    response = client.post("/auth/register", json=TEST_USER_CREATE.model_dump())
    assert response.status_code == 201

    model = UserRead.model_validate(response.json())
    assert model.email == TEST_USER_CREATE.email
    assert model.first_name == TEST_USER_CREATE.first_name
    assert model.last_name == TEST_USER_CREATE.last_name
    assert model.language_code == TEST_USER_CREATE.language_code
    assert model.role.value == UserRole.USER.value
    assert model.is_active is True
    assert model.is_superuser is False
    assert model.is_verified is False


def test_auth(client: TestClient):
    response = client.post("/auth/login", data=TEST_USER_LOGIN)
    assert response.status_code == 204

    assert response.cookies is not None
    assert "fastapiusersauth" in response.cookies


def test_auth_token(auth_headers: dict[str, str]):
    ...


def test_2fa(client: TestClient, auth_headers: dict[str, str]):
    response = client.post(
        "/auth/2fa",
        json=TEST_USER_2FA.model_dump(),
        headers=auth_headers
    )
    assert response.status_code == 200

    assert response.cookies is not None
    assert "app-2fa" in response.cookies


def test_2fa_token(two_fa_headers: dict[str, str]):
    ...
