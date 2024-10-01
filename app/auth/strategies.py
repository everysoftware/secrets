from fastapi_users.authentication import JWTStrategy

from app.auth.models import UserOrm
from app.config import settings


def get_jwt_strategy() -> JWTStrategy[UserOrm, int]:
    return JWTStrategy(
        secret=settings.app.auth_secret,
        lifetime_seconds=settings.app.auth_token_lifetime,
    )
