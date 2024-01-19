from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.auth import AuthService
from application.password import PasswordService
from application.user import UserService
from backend.infrastructure import User
from backend.infrastructure import async_session
from infrastructure.password import PasswordRepository
from infrastructure.user import UserRepository
from interfaces.rest.auth.base_config import current_user
from interfaces.rest.auth.dependencies import verified_user


async def user_service(
    session: AsyncSession = Depends(async_session), user: User = Depends(current_user)
) -> UserService:
    return UserService(UserRepository(session, user))


async def auth_service() -> AuthService:
    return AuthService()


async def password_service(
    user: User = Depends(verified_user),
    session: AsyncSession = Depends(async_session),
) -> PasswordService:
    return PasswordService(PasswordRepository(session, user))
