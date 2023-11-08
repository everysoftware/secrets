from .auth import router as auth_router
from .main import router as main_router
from .record import router as record_router
from .start import router as start_router
from .user import router as user_router

routers = (
    auth_router,
    main_router,
    start_router,
    user_router,
    record_router,
)

__all__ = ('routers',)
