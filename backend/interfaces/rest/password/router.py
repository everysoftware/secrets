from fastapi import APIRouter, Depends, status

from application.password import PasswordService
from domain.base import Page, Params
from domain.password import PasswordCreate, PasswordScheme, PasswordUpdate, PasswordItem
from interfaces.rest.dependencies import password_service
from interfaces.rest.password.dependencies import valid_password

router = APIRouter(prefix="/passwords", tags=["passwords"])


@router.post("", response_model=PasswordScheme, status_code=status.HTTP_201_CREATED)
async def create_password(
    password: PasswordCreate,
    service: PasswordService = Depends(password_service),
):
    return await service.create(password)


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
    return await service.update(password.id, update_password)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_password(
    password: PasswordScheme = Depends(valid_password),
    service: PasswordService = Depends(password_service),
):
    await service.delete(password.id)


@router.get("", response_model=Page[PasswordItem], status_code=status.HTTP_200_OK)
async def search_password(
    params: Params = Depends(),
    service: PasswordService = Depends(password_service),
):
    return await service.search(params)
