from fastapi import APIRouter, Depends, status

from src.api.dependencies import valid_password
from src.application.auth import get_current_user
from src.application.dependencies import get_password_service
from src.application.services import PasswordService
from src.domain.schemes import (
    SPasswordCreate,
    SUser,
    SPassword,
    SPasswordUpdate,
    SPasswordItem,
    SParams,
    SPage,
)

router = APIRouter(prefix="/passwords", tags=["passwords"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, description="Create a new password"
)
async def create_password(
    password: SPasswordCreate,
    user: SUser = Depends(get_current_user),
    service: PasswordService = Depends(get_password_service),
) -> SPassword:
    return await service.create(user, password)


@router.get(
    "/{item_id}",
    status_code=status.HTTP_200_OK,
    description="Get a password by id",
)
async def get_password(
    password: SPassword = Depends(valid_password),
) -> SPassword:
    return password


@router.patch(
    "/{item_id}",
    status_code=status.HTTP_200_OK,
    description="Update a password",
)
async def patch_password(
    update_password: SPasswordUpdate,
    password: SPassword = Depends(valid_password),
    service: PasswordService = Depends(get_password_service),
) -> SPassword:
    return await service.update(password, update_password)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a password",
)
async def delete_password(
    password: SPassword = Depends(valid_password),
    service: PasswordService = Depends(get_password_service),
) -> None:
    return await service.delete(password)


@router.get("", status_code=status.HTTP_200_OK, description="Search for passwords")
async def search_password(
    query: str | None = None,
    params: SParams = Depends(),
    user: SUser = Depends(get_current_user),
    service: PasswordService = Depends(get_password_service),
) -> SPage[SPasswordItem]:
    return await service.search(user, params, query)
