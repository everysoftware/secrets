from fastapi import APIRouter

from secrets_app.auth.backends import cookie_jwt_backend
from secrets_app.auth.dependencies import fastapi_users
from secrets_app.auth.schemas import SUser, SUserCreate

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(
    fastapi_users.get_register_router(SUser, SUserCreate),
)
router.include_router(fastapi_users.get_auth_router(cookie_jwt_backend))
