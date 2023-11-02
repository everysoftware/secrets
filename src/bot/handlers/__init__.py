from .auth import router as auth_router
from .confirmation import router as confirmation_router
from .forwarding import redirects
from .main import router as main_router
from .record_addition import router as record_addition_router
from .record_editing import router as record_editing_router
from .record_misc import router as record_misc_router
from .record_removal import router as record_removal_router
from .record_showing import router as record_showing_router
from .start import router as start_router

routers = (
    start_router,
    auth_router,
    main_router,
    confirmation_router,
    record_editing_router,
    record_addition_router,
    record_removal_router,
    record_showing_router,
    record_misc_router
)

__all__ = ('routers', 'redirects')
