from typing import Any

from fastapi_users import jwt
from jwt import InvalidTokenError
from starlette.requests import Request
from starlette.responses import Response

from common.settings import settings
from infrastructure.models import User
from interface.exceptions.auth import BadTwoFAToken, TwoFARequired

TOKEN_AUD = "fastapi-users"
TOKEN_COOKIE = "fastapi-2fa-auth"
TOKEN_HEADER = "Two-Factor-Authentication"


def create_token(user: User) -> str:
    to_encode = {"sub": user.id, "aud": TOKEN_AUD}
    return jwt.generate_jwt(
        to_encode,
        settings.auth.secret,
        lifetime_seconds=settings.auth.token_lifetime,
    )


def add_token_to_response(response: Response, token: str) -> None:
    response.set_cookie(
        key=TOKEN_COOKIE,
        value=token,
        httponly=True,
        secure=True,
        max_age=settings.auth.token_lifetime,
    )


def get_token_from_request(request: Request) -> str:
    token = request.cookies.get(TOKEN_COOKIE)

    if not token:
        token = request.headers.get(TOKEN_HEADER)

        if not token:
            raise TwoFARequired()

        if not token.startswith("Bearer "):
            raise BadTwoFAToken()
        token = token[7:]

    return token


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode_jwt(token, settings.auth.secret, [TOKEN_AUD])
    except (InvalidTokenError, ValueError):
        raise BadTwoFAToken()


def validate_payload(user: User, payload: dict[str, Any]) -> None:
    if payload["aud"] != TOKEN_AUD or payload["sub"] != user.id:
        raise BadTwoFAToken()
