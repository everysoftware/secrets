from .auth import auth_router
from .confirmation import confirmation_router
from .main import main_router
from .redirects import redirects
from .start import start_router

routers = (
    start_router,
    auth_router,
    main_router,
    confirmation_router
)

__all__ = ('routers', 'redirects')
