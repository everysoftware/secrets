from aiogram import types, Router, filters
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.middlewares import DatabaseMd
from bot.structures.fsm import LoginGroup, RegisterGroup
from bot.structures.keyboards import LOGIN_KB, REG_KB
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
            _('Привет! Я бот-менеджер паролей. Я надёжно защищу твои данные и буду хранить их в целости и '
              'сохранности. Чтобы зарегистрироваться нажми на кнопку внизу 👇'),
            reply_markup=REG_KB)
    else:
        await state.set_state(LoginGroup.button_step)
        msg = await msg.answer(
            _('Привет, {first_name} {last_name}, мы тебя помним! '
              'Чтобы авторизоваться нажми на кнопку внизу 👇').format(
                first_name=msg.from_user.first_name,
                last_name=msg.from_user.last_name),
            reply_markup=LOGIN_KB)

    return msg


@start_router.message(filters.Command('help'))
async def help_(msg: types.Message) -> Message:
    return await msg.answer(_('<b>Команды бота:</b>\n\n') + BOT_COMMANDS_STR)


@start_router.message(filters.Command('author'))
async def author(msg: types.Message) -> Message:
    return await msg.answer(_('Автор бота: @ivanstasevich 👨‍💻'))
