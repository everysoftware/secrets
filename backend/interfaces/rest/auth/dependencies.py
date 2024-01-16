from fastapi import Depends
from starlette.requests import Request

from application.auth import AuthService
from domain.user.schemes import TwoFALogin
from infrastructure import User
from .base_config import current_user
from .exceptions import WrongOTP, TwoFAAlreadyEnabled
from .two_fa import get_token_from_request, decode_token, validate_payload


async def non_two_fa_user(user: User = Depends(current_user)) -> User:
    if user.is_two_fa_enabled:
        raise TwoFAAlreadyEnabled()
    return user


async def check_otp(login: TwoFALogin, user: User = Depends(current_user)):
    if not AuthService.check_otp(user, login):
        raise WrongOTP()


async def verified_user(request: Request, user: User = Depends(current_user)) -> User:
    if user.is_two_fa_enabled:
        token = get_token_from_request(request)
        payload = decode_token(token)
        validate_payload(user, payload)

    return user
