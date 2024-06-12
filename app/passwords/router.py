from typing import Annotated

from fastapi import APIRouter, Depends, status, Query

from app.dependencies import GWDep
from app.passwords.dependencies import valid_password
from app.passwords.schemas import (
    SPasswordCreate,
    SPassword,
    SPasswordUpdate,
    SPasswordPage,
)
from app.schemas import PageParams

router = APIRouter(prefix="/passwords", tags=["Passwords"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    description="Create a new password",
)
async def create_password(
    creation: SPasswordCreate,
    gw: GWDep,
) -> SPassword:
    return await gw.passwords.create(creation)


@router.get(
    "/{password_id}",
    status_code=status.HTTP_200_OK,
    description="Get a password by id",
)
async def get_password(
    password: Annotated[SPassword, Depends(valid_password)],
) -> SPassword:
    return password


@router.patch(
    "/{password_id}",
    status_code=status.HTTP_200_OK,
    description="Update a password",
)
async def patch_password(
    update: SPasswordUpdate,
    password: Annotated[SPassword, Depends(valid_password)],
    gw: GWDep,
) -> SPassword:
    return await gw.passwords.update(password.id, update)


@router.delete(
    "/{password_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a password",
)
async def delete_password(
    password: Annotated[SPassword, Depends(valid_password)],
    gw: GWDep,
) -> None:
    return await gw.passwords.delete(password)


@router.get(
    "", status_code=status.HTTP_200_OK, description="Search for passwords"
)
async def search_password(
    params: Annotated[PageParams, Depends()],
    gw: GWDep,
    query: str | None = Query(None),
) -> SPasswordPage:
    return await gw.passwords.search(params, query)
