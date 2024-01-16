from typing import Any

import pytest
from httpx import AsyncClient

from schemes.record import RecordUpdate
from entities.records import (
    TEST_RECORDS_NEGATIVE,
    NOT_FOUND_RECORDS,
    NOT_FOUND_RECORDS_FOR_PATCH,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method,path",
    (
        ("get", "/records"),
        ("get", "/records/1"),
        ("post", "/records/create"),
        ("get", "/records/count"),
        ("patch", "/records/1"),
        ("delete", "/records/1"),
    ),
)
async def test_records_unauthorized(ac: AsyncClient, method: str, path: str) -> None:
    response = await ac.request(method, path)

    assert response.status_code == 401

    json = response.json()
    assert "detail" in json
    assert json["detail"] == "Unauthorized"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method,path",
    (
        ("get", "/records/1"),
        ("patch", "/records/1"),
        ("delete", "/records/1"),
    ),
)
async def test_records_unauthorized_2fa(
    ac: AsyncClient, auth_headers: dict[str, str], method: str, path: str
) -> None:
    response = await ac.request(method, path, headers=auth_headers)

    assert response.status_code == 401

    json = response.json()
    assert "detail" in json
    assert json["detail"] == "2FA is required"


@pytest.mark.asyncio
@pytest.mark.parametrize("record", TEST_RECORDS_NEGATIVE)
async def test_create_record_unprocessable_entity(
    ac: AsyncClient, auth_headers: dict[str, str], record: dict[str, Any]
) -> None:
    response = await ac.post("/records/create", json=record, headers=auth_headers)

    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method",
    (
        "get",
        "delete",
    ),
)
@pytest.mark.parametrize("record_id", NOT_FOUND_RECORDS)
async def test_records_not_found(
    ac: AsyncClient, two_fa_headers: dict[str, str], method: str, record_id: int
) -> None:
    response = await ac.request(method, f"/records/{record_id}", headers=two_fa_headers)

    assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize("record_id,record", NOT_FOUND_RECORDS_FOR_PATCH)
async def test_patch_record_not_found(
    ac: AsyncClient,
    two_fa_headers: dict[str, str],
    record_id: int,
    record: RecordUpdate,
) -> None:
    response = await ac.patch(
        f"/records/{record_id}", json=record.model_dump(), headers=two_fa_headers
    )

    assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "page,per_page",
    (
        (1, 0),
        (0, 1),
        (0, 0),
        (1, -1),
        (-1, 1),
        (-1, -1),
    ),
)
async def test_paginate_records_validation_error(
    ac: AsyncClient, auth_headers: dict[str, str], page: int, per_page: int
) -> None:
    response = await ac.get(
        "/records", params={"page": page, "per_page": per_page}, headers=auth_headers
    )

    assert response.status_code == 422
