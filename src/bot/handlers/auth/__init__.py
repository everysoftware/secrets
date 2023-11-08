from aiogram import Router

from .authorization import router as authorization_router
from .registration import router as registration_router
from ...middlewares import DatabaseMd

routers = (
    authorization_router,
    registration_router,
)

router = Router(name='auth')

router.include_routers(*routers)
router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

__all__ = ('router',)
