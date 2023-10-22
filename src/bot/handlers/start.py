from aiogram import types, Router, filters
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.middlewares import DatabaseMd
from bot.structures.fsm import LoginGroup, RegisterGroup
from bot.structures.keyboards import get_login_kb
from bot.structures.keyboards import get_reg_kb
from db import Database
from .commands import BOT_COMMANDS_STR

start_router = Router(name='start')

start_router.message.middleware(DatabaseMd())


@start_router.message(filters.Command('start'))
async def start(msg: types.Message, state: FSMContext, db: Database, command: CommandObject = None) -> Message:
    is_new = await db.user.get(msg.from_user.id) is None

    if is_new:
        await state.set_state(RegisterGroup.button_step)
        msg = await msg.answer(
            'Привет! Я бот-менеджер паролей. Я надёжно защищу твои данные и буду хранить их в целости и '
            'сохранности. Чтобы зарегистрироваться нажми на кнопку внизу 👇',
            reply_markup=get_reg_kb())
    else:
        await state.set_state(LoginGroup.button_step)
        msg = await msg.answer(
            f'Привет, {msg.from_user.first_name} {msg.from_user.last_name}, мы тебя помним! '
            f'Чтобы авторизоваться нажми на кнопку внизу 👇',
            reply_markup=get_login_kb())

    return msg


@start_router.message(filters.Command('help'))
async def help_(msg: types.Message) -> Message:
    return await msg.answer('<b>Команды бота:</b>\n\n' + BOT_COMMANDS_STR)


@start_router.message(filters.Command('author'))
async def author(msg: types.Message) -> Message:
    return await msg.answer('Автор бота: @ivanstasevich 👨‍💻')
