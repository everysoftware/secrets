from fastapi import Depends

from src.application.services import (
    AuthService,
    UserService,
    SecurityService,
    PasswordService,
)
from src.infrastructure.db import UnitOfWork


def get_auth_service(
    uow: UnitOfWork = Depends(),
) -> AuthService:
    return AuthService(uow)


def get_user_service(
    uow: UnitOfWork = Depends(),
) -> UserService:
    return UserService(uow)


def get_security_service(
    uow: UnitOfWork = Depends(),
) -> SecurityService:
    return SecurityService(uow)


def get_password_service(
    uow: UnitOfWork = Depends(),
    security: SecurityService = Depends(get_security_service),
) -> PasswordService:
    return PasswordService(uow, security)
