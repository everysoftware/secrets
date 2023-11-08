from aiogram import Router

from .confirm import router as confirmation_router
from .delete import router as delete_router
from .update import router as update_router
from ...filters import RegisterFilter
from ...middlewares import DatabaseMd

routers = (
    update_router,
    delete_router,
    confirmation_router
)

router = Router(name='user')
router.include_routers(*routers)

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

router.message.filter(RegisterFilter())
router.callback_query.filter(RegisterFilter())

__all__ = ('router',)