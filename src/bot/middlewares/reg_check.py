from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.structures.fsm import RegisterGroup
from bot.structures.keyboards import REG_KB
from cache import Cache
from db.database import Database


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

            user_exists = await cache.get(f'user_exists:{event.from_user.id}')
            if user_exists is None:
                async with session.begin():
                    user_exists = int(await data['db'].user.get(event.from_user.id) is not None)
                    await cache.set(
                        f'user_exists:{event.from_user.id}',
                        user_exists
                    )

            if user_exists:
                return await handler(event, data)
            else:
                return await self.reg_gate(event, data['state'])

    @staticmethod
    async def reg_gate(msg: types.Message, state: FSMContext):
        await msg.answer(
            'Ты не зарегистрирован. Чтобы зарегистрироваться нажми на кнопку внизу 👇',
            reply_markup=REG_KB)
        await state.set_state(RegisterGroup.button_step)
