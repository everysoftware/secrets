from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import jwt
from starlette import status
from starlette.responses import Response

from app.api.auth.base_config import (bearer_backend, cookie_backend,
                                      current_user, fastapi_users)
from app.api.auth.schemes import TwoFALogin, UserCreate, UserRead, UserUpdate
from app.api.utils import SHA256
from app.core.config import cfg
from app.core.models import User

router = APIRouter()

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_auth_router(cookie_backend), prefix="/auth", tags=["auth"]
)
router.include_router(
    fastapi_users.get_auth_router(bearer_backend), prefix="/auth-token", tags=["auth"]
)
router.include_router(
    fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"]
)
router.include_router(
    fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"]
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


async def create_2fa_token(user: User) -> str:
    to_encode = {"sub": user.id, "aud": "fastapi-users-auth", "type": "2fa"}
    encoded_jwt = jwt.generate_jwt(
        to_encode, cfg.api.secret_auth, lifetime_seconds=60 * 5
    )

    return encoded_jwt


@router.post(
    "/auth/2fa",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Bad credentials"},
    },
    tags=["auth"],
)
async def auth_2fa(
        credentials: TwoFALogin, response: Response, user: User = Depends(current_user)
):
    if SHA256.verify(credentials.master_password, user.hashed_master):
        response.set_cookie(
            key="app-2fa",
            value=await create_2fa_token(user),
            httponly=True,
            secure=True,
            max_age=60 * 5,  # 5 minutes
        )
        return {"detail": "2FA passed."}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad credentials"
        )


@router.post(
    "/auth-token/2fa",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Bad credentials"},
    },
    tags=["auth"],
)
async def auth_2fa_token(credentials: TwoFALogin, user: User = Depends(current_user)):
    if SHA256.verify(credentials.master_password, user.hashed_master):
        return {
            "access_token": await create_2fa_token(user),
            "token_type": "bearer",
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad credentials"
        )
