from fastapi import Depends
from starlette.requests import Request

from application.services import AuthService
from domain.schemes import UserScheme
from domain.schemes.dtos import TwoFALogin
from infrastructure.models import User
from interface.auth.base_config import current_user
from interface.exceptions.auth import WrongOTP, TwoFAAlreadyEnabled
from interface.auth.two_fa import get_token_from_request, decode_token, validate_payload


async def check_non_2fa(user: User = Depends(current_user)):
    if user.is_2fa_enabled:
        raise TwoFAAlreadyEnabled()


async def check_otp(login: TwoFALogin, user: User = Depends(current_user)):
    if not AuthService.check_otp(UserScheme.model_validate(user), login):
        raise WrongOTP()


async def verified_user(request: Request, user: User = Depends(current_user)) -> User:
    if user.is_2fa_enabled:
        token = get_token_from_request(request)
        payload = decode_token(token)
        validate_payload(user, payload)

    return user
