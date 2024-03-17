from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from src.domain.schemes import SUser
from src.infrastructure.config import log, settings
from src.infrastructure.mail import MWelcome, send_email_message
from src.application.auth.dependencies import UserOrm


class UserManager(IntegerIDMixin, BaseUserManager[UserOrm, int]):
    reset_password_token_secret = settings.app.auth_secret
    verification_token_secret = settings.app.auth_secret

    async def on_after_register(
        self, user: UserOrm, request: Request | None = None
    ) -> None:
        log.info(f"User {user.email} (#{user.id}) has registered")

        send_email_message(MWelcome(user=SUser.model_validate(user)).render())
