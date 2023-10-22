import asyncio
import logging
import sys

from aiogram import Bot

from bot.handlers import redirects
from bot.handlers.commands import BOT_COMMANDS
from cache import Cache
from config import cfg
from db import create_async_engine, get_session_maker
from dispatcher import create_dispatcher, get_redis_storage


async def main() -> None:
    logging.basicConfig(level=cfg.logging_level, stream=sys.stdout)

    bot = Bot(cfg.bot.tg_token, parse_mode='HTML')
    await bot.set_my_commands(BOT_COMMANDS)

    cache = Cache()
    storage = get_redis_storage(cache.client)
    engine = create_async_engine(cfg.db.build_connection_str())
    session_maker = get_session_maker(engine)

    dp = create_dispatcher(storage)

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        pool=session_maker,
        cache=cache,
        redirects=redirects
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot stopped')
