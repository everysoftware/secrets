from fastapi import APIRouter, Depends, status

from application.services import PasswordService
from domain.schemes.base import (
    Page,
    Params,
)
from domain.schemes.entities import UserScheme, PasswordScheme
from domain.schemes.transfer import PasswordCreate, PasswordUpdate, PasswordItem
from interfaces.dependencies.auth import authorized_user
from interfaces.dependencies.general import password_service
from interfaces.dependencies.password import valid_password

router = APIRouter(prefix="/passwords", tags=["passwords"])


@router.post("", response_model=PasswordScheme, status_code=status.HTTP_201_CREATED)
async def create_password(
    password: PasswordCreate,
    service: PasswordService = Depends(password_service),
    user: UserScheme = Depends(authorized_user),
):
    return await service.create(user, password)


@router.get(
    "/{item_id}",
    response_model=PasswordScheme,
    status_code=status.HTTP_200_OK,
)
async def get_password(
    password: PasswordScheme = Depends(valid_password),
):
    return password


@router.patch(
    "/{item_id}",
    response_model=PasswordScheme,
    status_code=status.HTTP_200_OK,
)
async def patch_password(
    update_password: PasswordUpdate,
    password: PasswordScheme = Depends(valid_password),
    service: PasswordService = Depends(password_service),
):
    return await service.update(password, update_password)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_password(
    password: PasswordScheme = Depends(valid_password),
    service: PasswordService = Depends(password_service),
):
    await service.delete(password)


@router.get("", response_model=Page[PasswordItem], status_code=status.HTTP_200_OK)
async def search_password(
    query: str | None = None,
    params: Params = Depends(),
    service: PasswordService = Depends(password_service),
    user: UserScheme = Depends(authorized_user),
):
    return await service.search(user, params, query)
