from aiogram import Router

from .get import router as get_router

routers = (get_router,)

router = Router()
router.include_routers(*routers)

__all__ = ("router",)
