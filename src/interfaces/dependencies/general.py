from fastapi import Depends

from application.services import UserService, AuthService, PasswordService
from infrastructure.utils import UnitOfWork


async def unit_of_work() -> UnitOfWork:
    return UnitOfWork()


async def user_service(
    uow: UnitOfWork = Depends(unit_of_work),
) -> UserService:
    return UserService(uow)


async def auth_service(
    uow: UnitOfWork = Depends(unit_of_work),
) -> AuthService:
    return AuthService(uow)


async def password_service(
    uow: UnitOfWork = Depends(unit_of_work),
) -> PasswordService:
    return PasswordService(uow)
