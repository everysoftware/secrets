import pytest
from httpx import AsyncClient

from schemes.record import RecordRead, RecordPage, RecordUpdate, RecordCreate
from application.utils import AES
from common.settings import cfg
from entities.records import (
    TOTAL_RECORDS,
    TEST_RECORDS,
    TEST_RECORDS_FOR_UPDATE,
    TOTAL_PAGES,
    PER_PAGE,
    PAGES,
)


def validate_record(
    model: RecordRead,
    plain_model: RecordCreate | RecordUpdate,
    record_id: int | None = None,
) -> None:
    if record_id is not None:
        assert model.id == record_id

    assert model.name == plain_model.name
    assert model.url == plain_model.url
    assert model.comment.text == plain_model.comment.text
    assert (
        AES.decrypt(model.username, cfg.api.secret_encryption) == plain_model.username
    )
    assert (
        AES.decrypt(model.password, cfg.api.secret_encryption) == plain_model.password
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("record_id,record", TEST_RECORDS)
async def test_create_record(
    ac: AsyncClient, auth_headers: dict[str, str], record_id: int, record: RecordCreate
) -> None:
    response = await ac.post(
        "/records/create", json=record.model_dump(), headers=auth_headers
    )

    assert response.status_code == 201
    model = RecordRead.model_validate(response.json())
    validate_record(model, record, record_id)


@pytest.mark.asyncio
@pytest.mark.parametrize("record_id,record", TEST_RECORDS)
async def test_get_record(
    ac: AsyncClient,
    two_fa_headers: dict[str, str],
    record_id: int,
    record: RecordCreate,
) -> None:
    response = await ac.get(f"/records/{record_id}", headers=two_fa_headers)

    assert response.status_code == 200

    model = RecordRead.model_validate(response.json())
    validate_record(model, record, record_id)


@pytest.mark.asyncio
@pytest.mark.parametrize("page,page_content", PAGES)
async def test_paginate_records(
    ac: AsyncClient,
    auth_headers: dict[str, str],
    page: int,
    page_content: list[tuple[int, RecordCreate]],
) -> None:
    response = await ac.get(
        "/records", params={"page": page, "per_page": PER_PAGE}, headers=auth_headers
    )

    assert response.status_code == 200

    model = RecordPage.model_validate(response.json())
    assert model.total == TOTAL_RECORDS
    assert model.page == page
    assert model.per_page == PER_PAGE
    assert model.pages == TOTAL_PAGES
    assert len(model.items) == min(PER_PAGE, TOTAL_RECORDS - (page - 1) * PER_PAGE)

    for record, (record_id, plain_record) in zip(model.items, page_content):
        validate_record(record, plain_record, record_id)


@pytest.mark.asyncio
@pytest.mark.parametrize("record_id,record", TEST_RECORDS_FOR_UPDATE)
async def test_patch_record(
    ac: AsyncClient,
    two_fa_headers: dict[str, str],
    record_id: int,
    record: RecordUpdate,
) -> None:
    response = await ac.patch(
        f"records/{record_id}", json=record.model_dump(), headers=two_fa_headers
    )

    assert response.status_code == 200

    model = RecordRead.model_validate(response.json())
    validate_record(model, record, record_id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "record_id",
    list(range(1, TOTAL_RECORDS + 1)),
)
async def test_delete_record(
    ac: AsyncClient, two_fa_headers: dict[str, str], record_id: int
) -> None:
    response = await ac.delete(f"records/{record_id}", headers=two_fa_headers)

    assert response.status_code == 200
    assert "detail" in response.json()
    assert response.json()["detail"] == "Record deleted successfully"
