from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender


class TypingMd(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:
        action = get_flag(data, 'chat_action')  # Check that handler marked with `typing` flag
        if not action:
            return await handler(event, data)

        async with ChatActionSender(
                bot=data['bot'],
                chat_id=event.chat.id,
                action=action
        ):
            return await handler(event, data)
