from typing import Sequence

from fastapi_users.authentication import (
    CookieTransport,
    Transport,
)

from app.config import settings

cookie_transport = CookieTransport(
    cookie_max_age=settings.app.auth_token_lifetime,
)

transports: Sequence[Transport] = [cookie_transport]
