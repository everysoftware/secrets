from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    BearerTransport,
    CookieTransport,
    JWTStrategy,
    AuthenticationBackend,
)

from application.auth.manager import get_user_manager
from common.settings import settings
from infrastructure.models import User
from interfaces.auth.strategies import JWTSecondStrategy

cookie_transport = CookieTransport(
    cookie_max_age=settings.auth.token_lifetime,
)
second_cookie_transport = CookieTransport(
    cookie_max_age=settings.auth.second_token_lifetime,
)
bearer_transport = BearerTransport("fill_me")

transports = [cookie_transport, bearer_transport]


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.auth.secret,
        lifetime_seconds=settings.auth.token_lifetime,
    )


def get_second_jwt_strategy() -> JWTSecondStrategy:
    return JWTSecondStrategy(
        secret=settings.auth.second_secret,
        lifetime_seconds=settings.auth.second_token_lifetime,
    )


cookie_backend = AuthenticationBackend(
    name="cookie_jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

second_cookie_backend = AuthenticationBackend(
    name="second_cookie_jwt",
    transport=second_cookie_transport,
    get_strategy=get_second_jwt_strategy,
)

bearer_backend = AuthenticationBackend(
    name="bearer_jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [cookie_backend, bearer_backend],
)
