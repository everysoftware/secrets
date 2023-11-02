import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from src.cache import Cache
from src.config import cfg
from src.db import create_async_engine, get_session_maker
from .api import generate_secret, on_startup, on_shutdown
from .dispatcher import create_dispatcher, create_redis_storage


def start_polling(bot: Bot, dp: Dispatcher) -> None:
    asyncio.run(dp.start_polling(bot))


def start_webhook(bot: Bot, dp: Dispatcher, secret: str) -> None:
    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=secret
    )

    webhook_requests_handler.register(app, path=cfg.webhook.path)
    setup_application(app, dp, bot=bot)

    web.run_app(app, host=cfg.webhook.host, port=cfg.webhook.port)


def main() -> None:
    logging.basicConfig(level=cfg.logging_level, stream=sys.stdout)

    bot = Bot(cfg.bot.tg_token, parse_mode='HTML')

    cache = Cache()
    storage = create_redis_storage(cache.client)
    session_maker = get_session_maker(create_async_engine(cfg.db.build_connection_str()))
    secret = generate_secret() if cfg.webhook.on else ''

    dp = create_dispatcher(
        storage,
        cache,
        session_maker,
        secret
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    if cfg.webhook.on:
        start_webhook(bot, dp, secret)
    else:
        start_polling(bot, dp)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot stopped')
