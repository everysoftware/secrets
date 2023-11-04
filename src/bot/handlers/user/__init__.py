from aiogram import Router

from .confirmation import router as confirmation_router
from .removal import router as removal_router
from .update import router as update_router
from ...filters import RegisterFilter
from ...middlewares import DatabaseMd

routers = (
    update_router,
    removal_router,
    confirmation_router
)

router = Router(name='user')
router.include_routers(*routers)

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

router.message.filter(RegisterFilter())
router.callback_query.filter(RegisterFilter())

__all__ = ('router',)
