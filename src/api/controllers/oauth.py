from fastapi import APIRouter

from src.application.auth import fastapi_users
from src.application.auth.config import bearer_backend

router = APIRouter(prefix="/oauth", tags=["oauth"])

router.include_router(fastapi_users.get_auth_router(bearer_backend))
