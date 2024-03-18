from .auth import router as auth_router
from .password import router as password_router
from .user import router as user_router
from .oauth import router as oauth_router

routers = [auth_router, user_router, oauth_router, password_router]

__all__ = ["routers"]
