from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import JWTStrategy
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from src.domain.schemes import SEnableTwoFactor, SUser
from src.infrastructure.db import async_session
from src.infrastructure.models import UserOrm
from .config import transports, backends
from .exceptions import SecondFactorAlreadyEnabled, SecondFactorRequired, WrongOTP
from .manager import UserManager
from .otp import validate_otp
from .two_factor import get_jwt_2factor_strategy, cookie_2factor_backend


async def get_user_db(
    session: AsyncSession = Depends(async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    """Get user database."""
    yield SQLAlchemyUserDatabase(session, UserOrm)


async def get_user_manager(
    user_db=Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    """Get user manager."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[UserOrm, int](
    get_user_manager,
    backends,
)

current_user = fastapi_users.current_user()


async def check_disabled_2fa(user: UserOrm = Depends(current_user)) -> None:
    """Check if second factor is disabled."""
    if user.two_factor:
        raise SecondFactorAlreadyEnabled()


async def check_otp(
    login: SEnableTwoFactor,
    user: UserOrm = Depends(current_user),
) -> UserOrm:
    """Check OTP."""
    if user.otp_secret is None:
        raise ValueError("OTP secret is not set.")

    if not validate_otp(login.otp, user.otp_secret):
        raise WrongOTP()

    return user


async def process_2fa(
    user: UserOrm = Depends(check_otp),
    strategy: JWTStrategy = Depends(get_jwt_2factor_strategy),
) -> Response:
    """Login two factor."""
    return await cookie_2factor_backend.login(strategy, user)


async def get_token(request: Request) -> str | None:
    """Get token from request."""
    for transport in transports:
        if callable(transport.scheme):
            token = await transport.scheme(request)

            if token:
                return token

    return None


async def get_current_user(
    user: UserOrm = Depends(current_user),
    user_manager: BaseUserManager = Depends(get_user_manager),
    token: str | None = Depends(get_token),
    strategy: JWTStrategy = Depends(get_jwt_2factor_strategy),
) -> SUser:
    """Get current user."""
    user_scheme = SUser.model_validate(user)

    if not user.two_factor:
        return user_scheme

    if not await strategy.read_token(token, user_manager):
        raise SecondFactorRequired()

    return user_scheme
