from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)

from app.auth.models import UserOrm
from app.config import settings

cookie_transport = CookieTransport(
    cookie_max_age=settings.app.auth_token_lifetime,
    cookie_samesite="none",
    cookie_domain=f".{settings.app_domain}",
)


def get_jwt_strategy() -> JWTStrategy[UserOrm, int]:
    return JWTStrategy(
        secret=settings.app.auth_secret,
        lifetime_seconds=settings.app.auth_token_lifetime,
    )


cookie_jwt_backend = AuthenticationBackend(
    name="cookie_jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
