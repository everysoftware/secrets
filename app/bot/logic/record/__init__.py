from aiogram import Router

from .create import router as add_router
from .delete import router as delete_router
from .edit import router as update_router
from .get import router as get_router
from .get_all import router as get_all_router
from ...middlewares import DatabaseMd

routers = (add_router, delete_router, get_router, update_router, get_all_router)

router = Router()
router.include_routers(*routers)

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())
