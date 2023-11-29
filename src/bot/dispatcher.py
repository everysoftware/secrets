import hashlib
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.redis import RedisStorage
from arq import create_pool
from redis.asyncio.client import Redis
from sqlalchemy.orm import sessionmaker

from src.bot.commands import BOT_COMMANDS
from src.bot.logic import routers
from src.bot.utils.callback_manager import manager
from src.cache import Cache
from src.config import cfg


def create_redis_storage(
        redis: Redis,
        state_ttl: int = cfg.redis.state_ttl,
        data_ttl: int = cfg.redis.data_ttl
) -> RedisStorage:
    return RedisStorage(redis=redis, state_ttl=state_ttl, data_ttl=data_ttl)


def generate_secret() -> str:
    return hashlib.sha256(os.urandom(16)).hexdigest()


async def on_startup(bot: Bot, dispatcher: Dispatcher, secret_token: str | None = None) -> None:
    await bot.set_my_commands(BOT_COMMANDS)
    dispatcher['rq'] = await create_pool(cfg.redis.pool_settings)

    await bot.delete_webhook()

    if cfg.webhook.on:
        if not secret_token:
            raise ValueError('secret_token must be provided')
        await bot.set_webhook(
            url=cfg.webhook.url,
            secret_token=secret_token
        )


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()


def create_dispatcher(
        storage: BaseStorage,
        cache: Cache,
        session_maker: sessionmaker,
) -> Dispatcher:
    dp = Dispatcher(
        storage=storage,
        cache=cache,
        pool=session_maker,
        manager=manager
    )

    if cfg.webhook.on:
        dp['secret_token'] = generate_secret()

    dp.include_routers(*routers)

    if cfg.mode != 'test':
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)

    return dp
