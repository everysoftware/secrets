from fastapi_users.authentication import AuthenticationBackend

from secrets_app.auth.strategies import get_jwt_strategy
from secrets_app.auth.transports import cookie_transport

cookie_jwt_backend = AuthenticationBackend(
    name="cookie_jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
