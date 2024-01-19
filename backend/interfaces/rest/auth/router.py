from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from application.auth import AuthService
from application.user import UserService
from backend.infrastructure import User
from domain.user.schemes import UserCreate, UserScheme
from interfaces.rest.auth.base_config import (
    bearer_backend,
    cookie_backend,
    current_user,
    fastapi_users,
)
from interfaces.rest.auth.dependencies import check_otp, check_non_2fa
from interfaces.rest.auth.two_fa import create_token, add_token_to_response
from interfaces.rest.dependencies import auth_service, user_service

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(
    fastapi_users.get_register_router(UserScheme, UserCreate),
)
router.include_router(fastapi_users.get_auth_router(cookie_backend))
router.include_router(fastapi_users.get_auth_router(bearer_backend), prefix="/bearer")
router.include_router(fastapi_users.get_reset_password_router())
router.include_router(fastapi_users.get_verify_router(UserScheme))


@router.post(
    "/enable-2fa", status_code=status.HTTP_200_OK, dependencies=[Depends(check_non_2fa)]
)
async def enable_two_factor(
    service: AuthService = Depends(auth_service),
    service_user: UserService = Depends(user_service),
):
    user_scheme = await service_user.update_otp_secret()
    qr_code = service.generate_otp_qr_code(user_scheme)
    return f"data:image/png;base64,{qr_code}"


@router.post(
    "/2fa",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_otp)],
)
async def auth_two_factor(
    response: Response,
    user: User = Depends(current_user),
    service_user: UserService = Depends(user_service),
):
    await service_user.enable_2fa()
    token = create_token(user)
    add_token_to_response(response, token)
