from fastapi import Depends, HTTPException
from fastapi_users import FastAPIUsers, jwt
from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)
from jwt import InvalidTokenError
from starlette import status
from starlette.requests import Request

from app.api.auth.manager import get_user_manager
from app.core.config import cfg
from app.core.models import User

cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=cfg.api.secret_auth, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


async def two_fa_verified(request: Request, user: User = Depends(current_user)):
    token = request.cookies.get("2fa")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="2fa is required")

    try:
        payload = jwt.decode_jwt(token, cfg.api.secret_auth, ["fastapi-users:auth"])
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad 2fa token")

    return payload['sub'] == user.id
