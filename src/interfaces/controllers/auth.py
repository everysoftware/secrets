from fastapi import APIRouter, Depends
from starlette import status

from application.services import UserService, AuthService
from domain.schemes.entities import UserScheme
from domain.schemes.transfer import UserCreate
from infrastructure.models import User
from interfaces.auth.base_config import (
    cookie_backend,
    fastapi_users,
    get_second_jwt_strategy,
    second_cookie_backend,
)
from interfaces.auth.strategies import SecondStrategy
from interfaces.dependencies.auth import check_disabled_2fa, check_otp, current_user
from interfaces.dependencies.general import auth_service, user_service

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(
    fastapi_users.get_register_router(UserScheme, UserCreate),
)
router.include_router(fastapi_users.get_auth_router(cookie_backend))
router.include_router(fastapi_users.get_reset_password_router())
router.include_router(fastapi_users.get_verify_router(UserScheme))


@router.post(
    "/enable-2fa",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_disabled_2fa)],
)
async def enable_2fa(
        service: AuthService = Depends(auth_service),
        service_user: UserService = Depends(user_service),
        user: User = Depends(current_user),
):
    user = await service_user.update_otp_secret(UserScheme.model_validate(user))
    qr_code = service.generate_otp_qr_code(user)
    return f"data:image/png;base64,{qr_code}"


@router.post(
    "/2fa",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_otp)],
)
async def auth_2fa(
        service_user: UserService = Depends(user_service),
        user: User = Depends(current_user),
        strategy: SecondStrategy = Depends(get_second_jwt_strategy),
):
    if not user.is_2fa_enabled and user.otp_secret:
        await service_user.enable_2fa(UserScheme.model_validate(user))

    return await second_cookie_backend.login(strategy, user)
