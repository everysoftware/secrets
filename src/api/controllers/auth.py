from fastapi import APIRouter, Depends
from starlette import status

from src.application.auth import (
    fastapi_users,
    cookie_backend,
    get_current_user,
    check_disabled_2fa,
    check_otp,
    process_2fa,
)
from src.application.dependencies import get_auth_service
from src.application.services import AuthService
from src.domain.schemes import SUser, SUserCreate, SQRCode

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(
    fastapi_users.get_register_router(SUser, SUserCreate),
)
router.include_router(fastapi_users.get_auth_router(cookie_backend))


@router.post(
    "/2fa/connect",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_disabled_2fa)],
    description=(
        "Returns a QR code to connect authenticator app, e.g. Google Authenticator."
        "This endpoint updates the user's secret key and resets the two-factor authentication."
    ),
)
async def connect(
    user: SUser = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
) -> SQRCode:
    return await service.connect_two_factor(user)


@router.post(
    "/2fa/enable",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_disabled_2fa), Depends(check_otp)],
    description="Enable two-factor authentication.",
)
async def enable_2fa(
    user: SUser = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
) -> SUser:
    return await service.enable_two_factor(user)


@router.post(
    "/2fa/login",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Login with two-factor authentication.",
)
async def login_2fa(
    response=Depends(process_2fa),
) -> None:
    return response
