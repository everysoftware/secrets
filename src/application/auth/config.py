from typing import Sequence

from fastapi_users.authentication import (
    BearerTransport,
    CookieTransport,
    JWTStrategy,
    AuthenticationBackend,
    Transport,
)

from src.infrastructure.config import settings

cookie_transport = CookieTransport(
    cookie_max_age=settings.app.auth_token_lifetime,
)

# TODO: Add the tokenUrl to the bearer transport
# For testing purposes, we must have a bearer authentication
bearer_transport = BearerTransport("fill_me")

transports: Sequence[Transport] = [cookie_transport, bearer_transport]


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.app.auth_secret,
        lifetime_seconds=settings.app.auth_token_lifetime,
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

backends = [cookie_backend, bearer_backend]
