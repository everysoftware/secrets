from aiogram import Router

from .authorize import router as authorize_router
from .logout import router as exit_router
from .register import router as register_router
from ...middlewares import DatabaseMd

routers = (authorize_router, register_router, exit_router)

router = Router()

router.include_routers(*routers)
router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

__all__ = ("router",)
