from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis import Redis

from src.bot.handlers import routers
from src.config import cfg


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

    for router in routers:
        dp.include_router(router)

    return dp
