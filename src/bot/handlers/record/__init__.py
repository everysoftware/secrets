from aiogram import Router

from .add import router as add_router
from .delete import router as delete_router
from .show import router as show_router
from .show_all import router as show_all_router
from .update import router as update_router
from ...middlewares import DatabaseMd

routers = (
    add_router,
    delete_router,
    show_router,
    update_router,
    show_all_router
)

router = Router(name='record')
router.include_routers(*routers)

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())
