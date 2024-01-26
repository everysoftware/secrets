from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from application.services import UserService, AuthService
from domain.schemes import UserScheme
from domain.schemes.dtos import UserCreate
from infrastructure.models import User
from interface.auth.base_config import (
    bearer_backend,
    cookie_backend,
    current_user,
    fastapi_users,
)
from interface.auth.two_fa import create_token, add_token_to_response
from interface.dependencies.auth import check_non_2fa, check_otp
from interface.dependencies.general import auth_service, user_service

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
async def auth_two_factor(
    response: Response,
    service_user: UserService = Depends(user_service),
    user: User = Depends(current_user),
):
    await service_user.enable_2fa(UserScheme.model_validate(user))
    token = create_token(user)
    add_token_to_response(response, token)
