from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from app.core import Database


class DatabaseMd(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery | TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, (Message, CallbackQuery)):
            raise ValueError(
                "Database middleware works only with messages and callback queries."
            )
        async with data["pool"]() as session:
            data["core"] = Database(session)
            return await handler(event, data)
