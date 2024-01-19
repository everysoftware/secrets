from typing import AsyncGenerator

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from domain.user import UserScheme
from infrastructure import async_session, async_session_factory
from infrastructure.auth import generate_secret
from infrastructure.mail import mail_templates
from infrastructure.tasks import send_email
from infrastructure.user import User
from interfaces.rest.config import rest_settings


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = rest_settings.auth.secret
    verification_token_secret = rest_settings.auth.secret

    async def on_after_register(self, user: User, request: Request | None = None):
        print(f"Пользователь {user.email} (#{user.id}) успешно зарегистрирован")

        send_email.delay(mail_templates.welcome(UserScheme.model_validate(user)))


async def get_user_db(session: AsyncSession = Depends(async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(
    user_db=Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)
