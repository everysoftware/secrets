from fastapi import APIRouter

from src.domain.schemes import SUser, SUserUpdate
from src.application.auth import fastapi_users

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(SUser, SUserUpdate),
    prefix="/users",
    tags=["users"],
)
