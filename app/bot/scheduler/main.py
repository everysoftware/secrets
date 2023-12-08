from aiogram import Bot
from core.config import cfg


async def startup(ctx) -> None:
    ctx["bot"] = Bot(token=cfg.bot.tg_token)


async def shutdown(ctx) -> None:
    await ctx["bot"].session.close()


async def send_message(ctx, chat_id: int, text: str) -> None:
    bot: Bot = ctx["bot"]
    await bot.send_message(chat_id, text)


async def delete_message(ctx, chat_id: int, message_id: int) -> None:
    bot: Bot = ctx["bot"]
    await bot.delete_message(chat_id, message_id)


class WorkerSettings:
    redis_settings = cfg.redis.pool_settings
    on_startup = startup
    on_shutdown = shutdown
    functions = [
        send_message,
        delete_message,
    ]
