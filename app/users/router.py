from fastapi import APIRouter

from app.auth.dependencies import fastapi_users
from app.auth.schemas import SUser, SUserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(SUser, SUserUpdate),
    prefix="/users",
    tags=["users"],
)
