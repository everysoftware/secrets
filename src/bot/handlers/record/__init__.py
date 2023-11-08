from aiogram import Router

from .add import router as creation_router
from .delete import router as removal_router
from .show import router as show_router
from .show_all import router as show_all_router
from .update import router as update_router
from ...filters import RegisterFilter
from ...middlewares import DatabaseMd

routers = (
    creation_router,
    removal_router,
    show_router,
    update_router,
    show_all_router
)

router = Router(name='record')
router.include_routers(*routers)

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

router.message.filter(RegisterFilter())
router.callback_query.filter(RegisterFilter())
