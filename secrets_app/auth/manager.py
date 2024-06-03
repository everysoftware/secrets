from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from secrets_app.auth.schemas import SUser
from secrets_app.mail import send_email_message, MWelcome
from secrets_app.settings import settings
from secrets_app.auth.models import UserOrm


class UserManager(IntegerIDMixin, BaseUserManager[UserOrm, int]):
    reset_password_token_secret = settings.app.auth_secret
    verification_token_secret = settings.app.auth_secret

    async def on_after_register(
        self, user: UserOrm, request: Request | None = None
    ) -> None:
        send_email_message(MWelcome(user=SUser.model_validate(user)).render())
