import hashlib
import os

from aiogram import Bot, Dispatcher
from arq import create_pool

from src.bot.handlers.commands import BOT_COMMANDS
from .config import cfg


def generate_secret() -> str:
    return hashlib.sha256(os.urandom(16)).hexdigest()


async def on_startup(bot: Bot, dispatcher: Dispatcher, secret_token: str) -> None:
    await bot.set_my_commands(BOT_COMMANDS)
    dispatcher['arq_redis'] = await create_pool(cfg.redis.pool_settings)

    await bot.delete_webhook()

    if cfg.webhook.on:
        await bot.set_webhook(
            url=cfg.webhook.url,
            secret_token=secret_token
        )


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()
