from fastapi import APIRouter

from domain.schemes.entities import UserScheme
from domain.schemes.transfer import UserUpdate
from interfaces.auth.base_config import fastapi_users

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserScheme, UserUpdate),
    prefix="/users",
    tags=["users"],
)
