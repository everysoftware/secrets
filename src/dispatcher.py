from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis import Redis
from sqlalchemy.orm import sessionmaker

from src.cache import Cache
from src.bot.handlers import routers, redirects
from src.config import cfg


def create_redis_storage(
        redis: Redis,
        state_ttl: int = cfg.redis.state_ttl,
        data_ttl: int = cfg.redis.data_ttl
) -> RedisStorage:
    return RedisStorage(redis=redis, state_ttl=state_ttl, data_ttl=data_ttl)


def create_dispatcher(
        storage: BaseStorage,
        cache: Cache,
        session_maker: sessionmaker,
        secret_token: str = ''
) -> Dispatcher:
    dp = Dispatcher(
        storage=storage,
        cache=cache,
        pool=session_maker,
        secret_token=secret_token,
        redirects=redirects
    )

    for router in routers:
        dp.include_router(router)

    return dp
