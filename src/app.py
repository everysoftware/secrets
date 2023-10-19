import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis

from cache import Cache
from config import cfg
from db import create_async_engine, get_session_maker
from handlers import routers, redirects
from handlers.commands import BOT_COMMANDS


def get_redis_storage(redis: Redis, state_ttl: int = cfg.redis.state_ttl, data_ttl: int = cfg.redis.data_ttl):
    return RedisStorage(redis=redis, state_ttl=state_ttl, data_ttl=data_ttl)


async def main() -> None:
    logging.basicConfig(level=cfg.logging_level, stream=sys.stdout)

    bot = Bot(cfg.bot.tg_token, parse_mode='HTML')
    await bot.set_my_commands(BOT_COMMANDS)

    cache = Cache()
    storage = get_redis_storage(cache.client)
    engine = create_async_engine(cfg.db.build_connection_str())
    session_maker = get_session_maker(engine)

    dp = Dispatcher(
        storage=storage
    )

    for router in routers:
        dp.include_router(router)

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        session_maker=session_maker,
        cache=cache,
        redirects=redirects
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot stopped')
