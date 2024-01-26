from fastapi import APIRouter

from domain.schemes import UserScheme
from domain.schemes.dtos import UserUpdate
from interface.auth.base_config import fastapi_users

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserScheme, UserUpdate),
    prefix="/users",
    tags=["users"],
)
