from starlette.testclient import TestClient

from schemes.user import UserCreate
from entities.auth import get_login_data, get_2fa_data


def test_auth(client: TestClient, user: UserCreate):
    response = client.post("/auth/login", data=get_login_data(user))
    assert response.status_code == 204

    assert response.cookies is not None
    assert "fastapiusersauth" in response.cookies


def test_2fa(client: TestClient, user: UserCreate, auth_headers: dict[str, str]):
    response = client.post(
        "/auth/2fa", json=get_2fa_data(user).model_dump(), headers=auth_headers
    )
    assert response.status_code == 200

    assert response.cookies is not None
    assert "app-2fa" in response.cookies


"""
def test_logout(client: TestClient, auth_headers: dict[str, str]):
    response = client.post(
        "/auth/logout",
        headers=auth_headers
    )
    assert response.status_code == 204

    assert not response.cookies
"""
