from aiogram import Router

from .creation import router as creation_router
from .misc import router as misc_router
from .removal import router as removal_router
from .show import router as show_router
from .update import router as update_router
from ...filters import RegisterFilter
from ...middlewares import DatabaseMd

routers = (
    creation_router,
    misc_router,
    removal_router,
    show_router,
    update_router
)

router = Router(name='record')
router.include_routers(*routers)

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

router.message.filter(RegisterFilter())
router.callback_query.filter(RegisterFilter())
