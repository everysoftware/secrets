import pytest
from httpx import AsyncClient

from api.records.schemes import RecordRead, RecordsRead, RecordUpdate, RecordCreate
from api.utils import AES
from core.config import cfg
from tests.utils.entities import TEST_RECORD_CREATE, TEST_RECORD_UPDATE

TOTAL_RECORDS = 10


def validate_record(
        model: RecordRead,
        record_id: int | None = None,
        plain_model: RecordCreate | RecordUpdate = TEST_RECORD_CREATE
) -> None:
    if record_id is not None:
        assert model.id == record_id

    assert model.name == plain_model.name
    assert model.url == plain_model.url
    assert model.comment.text == plain_model.comment.text
    assert AES.decrypt(model.username, cfg.api.secret_encryption) == plain_model.username
    assert AES.decrypt(model.password, cfg.api.secret_encryption) == plain_model.password


@pytest.mark.asyncio
async def test_create_record(ac: AsyncClient, auth_headers: dict[str, str]) -> None:
    for i in range(TOTAL_RECORDS):
        response = await ac.post(
            "/records/create",
            json=TEST_RECORD_CREATE.model_dump(),
            headers=auth_headers
        )

        assert response.status_code == 201
        model = RecordRead.model_validate(response.json())
        validate_record(model, i + 1)


@pytest.mark.asyncio
async def test_get_record(ac: AsyncClient, two_fa_headers: dict[str, str]) -> None:
    response = await ac.get(
        "/records/1",
        headers=two_fa_headers
    )

    assert response.status_code == 200

    model = RecordRead.model_validate(response.json())
    assert model.id == 1
    assert model.name == TEST_RECORD_CREATE.name
    assert model.url == TEST_RECORD_CREATE.url
    assert model.comment.text == TEST_RECORD_CREATE.comment.text
    assert AES.decrypt(model.username, cfg.api.secret_encryption) == TEST_RECORD_CREATE.username
    assert AES.decrypt(model.password, cfg.api.secret_encryption) == TEST_RECORD_CREATE.password


@pytest.mark.asyncio
async def test_get_record_not_found(ac: AsyncClient, two_fa_headers: dict[str, str]) -> None:
    response = await ac.get(
        f"/records/{TOTAL_RECORDS + 1}",
        headers=two_fa_headers
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_paginate_records(ac: AsyncClient, auth_headers) -> None:
    per_page = 3

    pages = TOTAL_RECORDS // per_page + (TOTAL_RECORDS % per_page > 0)
    for page in range(1, pages + 1):
        response = await ac.get(
            "/records",
            params={"page": page, "per_page": per_page},
            headers=auth_headers
        )

        assert response.status_code == 200

        model = RecordsRead.model_validate(response.json())
        assert model.total == TOTAL_RECORDS
        assert model.page == page
        assert model.per_page == per_page
        assert model.pages == pages
        assert len(model.items) == min(per_page, TOTAL_RECORDS - (page - 1) * per_page)

        for j, record in enumerate(model.items):
            validate_record(record)


@pytest.mark.asyncio
async def test_patch_record(ac: AsyncClient, two_fa_headers: dict[str, str]) -> None:
    response = await ac.patch(
        f"records/1",
        json=TEST_RECORD_UPDATE.model_dump(),
        headers=two_fa_headers
    )

    assert response.status_code == 200

    model = RecordRead.model_validate(response.json())
    validate_record(model, 1, TEST_RECORD_UPDATE)


@pytest.mark.asyncio
async def test_delete_record(ac: AsyncClient, two_fa_headers: dict[str, str]) -> None:
    response = await ac.delete(
        "records/1",
        headers=two_fa_headers
    )

    assert response.status_code == 200
    assert "detail" in response.json()
    assert response.json()["detail"] == "Record deleted successfully"
