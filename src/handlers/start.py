from aiogram import types, Router, filters
from aiogram.fsm.context import FSMContext

from db import Database
from keyboards import get_reg_kb
from src.fsm.auth import LoginGroup, RegisterGroup
from src.keyboards import get_login_kb
from src.middlewares import DatabaseMd
from .commands import BOT_COMMANDS_STR

start_router = Router(name='start')

start_router.message.middleware(DatabaseMd())


@start_router.message(filters.Command('start'))
async def start(msg: types.Message, state: FSMContext, db: Database) -> None:
    is_new = await db.user.get(msg.from_user.id) is None
    if is_new:
        await msg.answer(
            'Привет! Я бот-менеджер паролей. Я надёжно защищу твои данные и буду хранить их в целости и '
            'сохранности. Чтобы зарегистрироваться нажми на кнопку внизу 👇',
            reply_markup=get_reg_kb())
        await state.set_state(RegisterGroup.button_step)
    else:
        await msg.answer(f'Привет, {msg.from_user.first_name} {msg.from_user.last_name}, мы тебя помним! '
                         f'Чтобы авторизоваться нажми на кнопку внизу 👇',
                         reply_markup=get_login_kb())
        await state.set_state(LoginGroup.button_step)


@start_router.message(filters.Command('help'))
async def help_(msg: types.Message) -> None:
    await msg.answer('<b>Список команд</b>\n\n' + BOT_COMMANDS_STR)


@start_router.message(filters.Command('author'))
async def author(msg: types.Message) -> None:
    await msg.answer('Автор бота: @ivanstasevich 👨‍💻')
