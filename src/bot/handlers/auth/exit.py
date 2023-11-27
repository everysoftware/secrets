from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.middlewares import DatabaseMd

router = Router()

router.message.middleware(DatabaseMd())


@router.message(Command('exit'))
async def logout(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        'Вы успешно вышли из аккаунта ✅\n\n'
        'Если Вы хотите вернуться, пишите /start. Мы всегда будем рады Вас видеть! 🤗',
        reply_markup=types.ReplyKeyboardRemove()
    )
