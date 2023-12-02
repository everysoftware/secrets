from aiogram import Router

from ...middlewares import DatabaseMd
from .delete import router as delete_router
from .get import router as get_router
from .update import router as update_router
from .verify_id import router as verify_id_router

routers = (update_router, delete_router, verify_id_router, get_router)

router = Router()
router.include_routers(*routers)

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

__all__ = ("router",)
