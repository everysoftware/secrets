from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy,
)

from backend.infrastructure import User
from infrastructure.user.manager import get_user_manager
from interfaces.rest.config import rest_settings

cookie_transport = CookieTransport(cookie_max_age=rest_settings.auth.token_lifetime)
bearer_transport = BearerTransport("bearer-auth/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=rest_settings.auth.secret,
        lifetime_seconds=rest_settings.auth.token_lifetime,
    )


cookie_backend = AuthenticationBackend(
    name="cookie_jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
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

current_user = fastapi_users.current_user()
