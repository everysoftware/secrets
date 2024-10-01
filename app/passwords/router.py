from typing import Annotated

from fastapi import APIRouter, Depends, status, Query

from app.auth.dependencies import MeDep
from app.db.schemas import PageParams
from app.passwords.dependencies import valid_password, PasswordServiceDep
from app.passwords.schemas import (
    SPasswordCreate,
    SPasswordRead,
    SPasswordUpdate,
    SPasswordPage,
)

router = APIRouter(prefix="/passwords", tags=["Passwords"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    description="Create a new password",
)
async def create_password(
    creation: SPasswordCreate,
    user: MeDep,
    service: PasswordServiceDep,
) -> SPasswordRead:
    return await service.create(user, creation)


@router.get(
    "/{password_id}",
    status_code=status.HTTP_200_OK,
    description="Get a password by id",
)
async def get_password(
    password: Annotated[SPasswordRead, Depends(valid_password)],
) -> SPasswordRead:
    return password


@router.patch(
    "/{password_id}",
    status_code=status.HTTP_200_OK,
    description="Update a password",
)
async def patch_password(
    service: PasswordServiceDep,
    update: SPasswordUpdate,
    password: Annotated[SPasswordRead, Depends(valid_password)],
) -> SPasswordRead:
    return await service.update(password, update)


@router.delete(
    "/{password_id}",
    status_code=status.HTTP_200_OK,
    description="Delete a password",
)
async def delete_password(
    service: PasswordServiceDep,
    password: Annotated[SPasswordRead, Depends(valid_password)],
) -> SPasswordRead:
    return await service.delete(password)


@router.get(
    "", status_code=status.HTTP_200_OK, description="Search for passwords"
)
async def search_password(
    service: PasswordServiceDep,
    params: Annotated[PageParams, Depends()],
    user: MeDep,
    query: str | None = Query(None),
) -> SPasswordPage:
    return await service.search(user, params, query)
