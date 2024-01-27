from fastapi import Depends
from starlette.requests import Request

from application.auth.manager import UserManager, get_user_manager
from application.services import AuthService
from domain.schemes.entities import UserScheme
from infrastructure.models import User
from interfaces.auth.base_config import (
    fastapi_users,
    get_second_jwt_strategy,
    transports,
)
from interfaces.auth.schemes import TwoFALogin
from interfaces.auth.strategies import SecondStrategy
from interfaces.exceptions.auth import (
    WrongOTP,
    TwoFAAlreadyEnabled,
    SecondStageRequired,
)

current_user = fastapi_users.current_user()


async def check_disabled_2fa(user: User = Depends(current_user)):
    if user.is_2fa_enabled:
        raise TwoFAAlreadyEnabled()


async def check_otp(login: TwoFALogin, user: User = Depends(current_user)):
    if not AuthService.check_otp(UserScheme.model_validate(user), login):
        raise WrongOTP()


async def get_token(request: Request) -> str | None:
    for transport in transports:
        token = await transport.scheme(request)

        if token:
            return token

    return None


async def authorized_user(
    request: Request,
    user: User = Depends(current_user),
    strategy: SecondStrategy = Depends(get_second_jwt_strategy),
    user_manager: UserManager = Depends(get_user_manager),
) -> User:
    if not user.is_2fa_enabled:
        return user

    token = await get_token(request)
    if not await strategy.read_token(token, user_manager):
        raise SecondStageRequired()

    return user
