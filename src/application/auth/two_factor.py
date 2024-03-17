from fastapi_users.authentication import AuthenticationBackend, CookieTransport

from src.infrastructure.config import settings
from .strategies import JWT2FactorStrategy


def get_jwt_2factor_strategy() -> JWT2FactorStrategy:
    return JWT2FactorStrategy(
        secret=settings.app.auth_second_secret,
        lifetime_seconds=settings.app.auth_second_token_lifetime,
    )


cookie_transport = CookieTransport(
    cookie_max_age=settings.app.auth_second_token_lifetime,
)

cookie_2factor_backend = AuthenticationBackend(
    name="second_cookie_jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_2factor_strategy,
)
