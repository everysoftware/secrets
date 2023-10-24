from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from redis import Redis

from bot.handlers import routers
from config import cfg
from utils import WORKDIR


def get_redis_storage(
        redis: Redis,
        state_ttl: int = cfg.redis.state_ttl,
        data_ttl: int = cfg.redis.data_ttl
) -> RedisStorage:
    return RedisStorage(redis=redis, state_ttl=state_ttl, data_ttl=data_ttl)


def create_dispatcher(storage: BaseStorage) -> Dispatcher:
    dp = Dispatcher(
        storage=storage
    )

    i18n = I18n(path=WORKDIR / 'locales', default_locale='ru', domain='messages')
    i18n_md = SimpleI18nMiddleware(i18n=i18n)

    dp.message.middleware(i18n_md)
    dp.callback_query.middleware(i18n_md)

    for router in routers:
        dp.include_router(router)

    return dp
