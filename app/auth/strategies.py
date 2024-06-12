from fastapi_users.authentication import JWTStrategy

from app.settings import settings


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.app.auth_secret,
        lifetime_seconds=settings.app.auth_token_lifetime,
    )
