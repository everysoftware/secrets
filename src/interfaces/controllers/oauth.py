from fastapi import APIRouter

from interfaces.auth.base_config import fastapi_users, bearer_backend

router = APIRouter(prefix="/oauth", tags=["oauth"])

router.include_router(fastapi_users.get_auth_router(bearer_backend))
