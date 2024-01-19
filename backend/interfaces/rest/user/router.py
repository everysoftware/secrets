from fastapi import APIRouter

from domain.user import UserScheme, UserUpdate
from interfaces.rest.auth.base_config import fastapi_users

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserScheme, UserUpdate),
    prefix="/users",
    tags=["users"],
)
