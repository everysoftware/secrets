from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message, TelegramObject
from aiogram.utils.chat_action import ChatActionSender


class TypingMd(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            raise ValueError("Typing middleware works only with messages.")
        action = get_flag(
            data, "chat_action"
        )  # Check that handler marked with `typing` flag
        if not action:
            return await handler(event, data)

        async with ChatActionSender(
            bot=data["bot"], chat_id=event.chat.id, action=action
        ):
            return await handler(event, data)
