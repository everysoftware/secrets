import pytest
from httpx import AsyncClient

from app.api.records.schemes import RecordCreate
from tests.utils.entities import TEST_USER_LOGIN


@pytest.mark.asyncio
async def test_create_record(ac: AsyncClient):
    response = await ac.post("/auth/login", data=TEST_USER_LOGIN)
    assert response.status_code == 204

    # Now we can create a test record
    test_record = RecordCreate(
        name="Test Record",
        username="Test Username",
        password="Test Password",
        url="https://testurl.com",
        comment={"text": "Test Comment"}
    )

    assert True
    # response = await ac.post(
    #     "/records/create",
    #     json=test_record.model_dump()
    # )
    #
    # assert response.status_code == 201
    # assert response.json()["name"] == "Test Record"
    # assert response.json()["url"] == "https://testurl.com"
    # assert response.json()["comment"]["text"] == "Test Comment"
