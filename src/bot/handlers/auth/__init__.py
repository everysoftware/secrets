from aiogram import Router

from .authorize import router as authorize_router
from .register import router as register_router
from ...middlewares import DatabaseMd

routers = (
    authorize_router,
    register_router,
)

router = Router(name='auth')

router.include_routers(*routers)
router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

__all__ = ('router',)
