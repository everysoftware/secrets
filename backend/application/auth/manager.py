from typing import AsyncGenerator

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from common.log import log
from common.settings import settings
from domain.schemes import UserScheme
from infrastructure.database import async_session
from infrastructure.mail import mail_templates
from infrastructure.models import User
from infrastructure.tasks import send_email


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.auth.secret
    verification_token_secret = settings.auth.secret

    async def on_after_register(self, user: User, request: Request | None = None):
        log.info(f"User {user.email} (#{user.id}) has registered")

        send_email.delay(mail_templates.welcome(UserScheme.model_validate(user)))


async def get_user_db(session: AsyncSession = Depends(async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(
    user_db=Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)
