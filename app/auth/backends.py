from fastapi_users.authentication import AuthenticationBackend

from app.auth.strategies import get_jwt_strategy
from app.auth.transports import cookie_transport

cookie_jwt_backend = AuthenticationBackend(
    name="cookie_jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
