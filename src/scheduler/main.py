from contextlib import suppress

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from src.config import cfg


async def startup(ctx) -> None:
    ctx['bot'] = Bot(token=cfg.bot.tg_token)


async def shutdown(ctx) -> None:
    await ctx['bot'].session.close()


async def send_message(ctx, chat_id: int, text: str) -> None:
    bot: Bot = ctx['bot']
    await bot.send_message(chat_id, text)


async def delete_message(ctx, chat_id: int, message_id: int) -> None:
    bot: Bot = ctx['bot']
    await bot.delete_message(chat_id, message_id)


async def delete_record_message(ctx, chat_id: int, record_msg_id: int, cp_msg_id: int) -> None:
    bot: Bot = ctx['bot']
    with suppress(TelegramBadRequest):
        await bot.delete_message(chat_id, record_msg_id)
        await bot.delete_message(chat_id, cp_msg_id)


class WorkerSettings:
    redis_settings = cfg.redis.pool_settings
    on_startup = startup
    on_shutdown = shutdown
    functions = [
        send_message,
        delete_message,
        delete_record_message
    ]
