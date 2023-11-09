from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from src.cache import Cache
from src.db.database import Database


class RegisterCheck(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        cache: Cache = data['cache']

        async with data['pool']() as session:
            db = Database(session)
            data['db'] = db

            user_exists = await cache.get(f'user_exists:{event.from_user.id}', int)
            if user_exists is None:
                async with session.begin():
                    user_exists = int(await data['db'].user.get(event.from_user.id) is not None)

                await cache.set(
                    f'user_exists:{event.from_user.id}',
                    user_exists
                )

            return await handler(event, data)
