from starlette.testclient import TestClient

from utils.entities import TEST_USER_CREATE, TEST_USER_LOGIN


def test_register(client: TestClient):
    response = client.post("/auth/register", json=TEST_USER_CREATE.model_dump())
    assert response.status_code == 201


def test_auth(client: TestClient):
    response = client.post("/auth/login", data=TEST_USER_LOGIN)
    assert response.status_code == 204
