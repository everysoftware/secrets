from aiogram import types, Router
from aiogram.filters import CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.middlewares import RegisterCheck
from src.bot.structures.fsm import LoginGroup, RegisterGroup
from src.bot.structures.keyboards import LOGIN_KB, REG_KB
from src.cache import Cache
from .commands import BOT_COMMANDS_STR

start_router = Router(name='start')

start_router.message.middleware(RegisterCheck())


@start_router.message(Command('start'))
async def start(
        msg: types.Message,
        state: FSMContext,
        cache: Cache,
        command: CommandObject = None,
) -> Message:
    if await cache.get(f'user_exists:{msg.from_user.id}', int):
        await state.set_state(LoginGroup.waiting_for_click)
        msg = await msg.answer(
            'Привет, {first_name} {last_name}, мы тебя помним! '
            'Нажми на кнопку внизу, чтобы войти в аккаунт 👇'.format(
                first_name=msg.from_user.first_name,
                last_name=msg.from_user.last_name),
            reply_markup=LOGIN_KB)

    else:
        await state.set_state(RegisterGroup.waiting_for_click)
        msg = await msg.answer(
            'Привет! Я бот, позволяющий безопасно хранить твои пароли в Телеграм. '
            'Нажми на кнопку внизу, чтобы создать аккаунт 👇',
            reply_markup=REG_KB)

    return msg


@start_router.message(Command('help'))
async def help_(msg: types.Message) -> Message:
    return await msg.answer('<b>Команды бота:</b>\n\n' + BOT_COMMANDS_STR)


@start_router.message(Command('author'))
async def author(msg: types.Message) -> Message:
    return await msg.answer('Автор бота: @ivanstasevich 👨‍💻')
