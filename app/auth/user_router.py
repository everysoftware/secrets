from fastapi import APIRouter

from app.auth.dependencies import fastapi_users
from app.auth.schemas import SUserRead, SUserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(SUserRead, SUserUpdate),
    prefix="/users",
    tags=["users"],
)
