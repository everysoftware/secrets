from typing import Optional

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.orm import sessionmaker

from src.bot.structures.fsm import RegisterGroup
from src.bot.structures.keyboards import REG_KB
from src.cache import Cache
from src.db import Database


class RegisterFilter(Filter):
    async def __call__(
            self,
            event: Message | CallbackQuery,
            state: Optional[FSMContext] = None,
            cache: Optional[Cache] = None,
            pool: Optional[sessionmaker] = None,
    ) -> bool:
        if isinstance(event, Message):
            message = event
        elif isinstance(event, CallbackQuery):
            message = event.message
        else:
            raise ValueError

        if any(i is None for i in (state, cache, pool)):
            return False

        user_exists = await cache.get(f'user_exists:{event.from_user.id}', int)
        if user_exists is None:
            async with pool() as session:
                db = Database(session)
                async with session.begin():
                    user_exists = int(await db.user.get(event.from_user.id) is not None)

            await cache.set(
                f'user_exists:{event.from_user.id}',
                user_exists
            )

        if user_exists:
            return True

        if await state.get_state() not in RegisterGroup:
            await message.answer(
                'Для совершения этого действия тебе необходимо зарегистрироваться 👇',
                reply_markup=REG_KB
            )
            await state.set_state(RegisterGroup.waiting_for_click)

        return False
