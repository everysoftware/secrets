from fastapi import APIRouter, Depends, status

from application.services import PasswordService
from domain.schemes import (
    Page,
    Params,
    PasswordScheme,
    UserScheme,
)
from domain.schemes.dtos import PasswordCreate, PasswordUpdate, PasswordItem
from interface.dependencies.auth import verified_user
from interface.dependencies.general import password_service
from interface.dependencies.password import valid_password

router = APIRouter(prefix="/passwords", tags=["passwords"])


@router.post("", response_model=PasswordScheme, status_code=status.HTTP_201_CREATED)
async def create_password(
    password: PasswordCreate,
    service: PasswordService = Depends(password_service),
    user: UserScheme = Depends(verified_user),
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
    params: Params = Depends(),
    service: PasswordService = Depends(password_service),
    user: UserScheme = Depends(verified_user),
):
    return await service.search(user, params)
