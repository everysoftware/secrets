from fastapi import Depends, HTTPException
from fastapi_users import FastAPIUsers, jwt
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, CookieTransport,
                                          JWTStrategy)
from jwt import InvalidTokenError
from starlette import status
from starlette.requests import Request

from app.api.auth.manager import get_user_manager
from app.core.config import cfg
from app.core.models import User

cookie_transport = CookieTransport(cookie_max_age=3600)
bearer_transport = BearerTransport("auth-token/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=cfg.api.secret_auth, lifetime_seconds=3600)


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


async def two_fa_verified(request: Request, user: User = Depends(current_user)):
    token = request.cookies.get("app-2fa")

    if not token:
        token = request.headers.get("2FA")

        if not token.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad 2FA token"
            )
        token = token[7:]

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="2FA is required"
        )

    try:
        payload = jwt.decode_jwt(token, cfg.api.secret_auth, ["fastapi-users-auth"])
        if payload["sub"] != user.id:
            raise ValueError
    except (InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad 2FA token"
        )

    return user
