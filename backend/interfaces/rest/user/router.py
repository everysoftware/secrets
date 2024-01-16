from fastapi import APIRouter

from domain.user import UserRead, UserUpdate
from interfaces.rest.auth.base_config import fastapi_users

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
