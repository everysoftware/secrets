from fastapi_users import BaseUserManager, IntegerIDMixin

from app.auth.models import UserOrm
from app.config import settings


class UserManager(IntegerIDMixin, BaseUserManager[UserOrm, int]):
    reset_password_token_secret = settings.app.auth_secret
    verification_token_secret = settings.app.auth_secret
