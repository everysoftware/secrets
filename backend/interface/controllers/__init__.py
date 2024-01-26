from .auth import router as auth_router
from .password import router as password_router
from .user import router as user_router

routers = (password_router, auth_router, user_router)

__all__ = ["routers"]
