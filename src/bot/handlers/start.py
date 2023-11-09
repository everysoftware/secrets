from datetime import timedelta

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from arq import ArqRedis

from src.bot.fsm import LoginGroup, RegisterGroup
from src.bot.keyboards.auth import LOGIN_KB, REG_KB
from src.bot.middlewares import RegisterCheck
from src.cache import Cache
from .commands import BOT_COMMANDS_STR
from ..encryption import generate_password

router = Router(name='start')

router.message.middleware(RegisterCheck())


@router.message(Command('start'))
@router.message(Command('exit'))
async def start(
        message: types.Message,
        state: FSMContext,
        cache: Cache,
) -> Message:
    await state.clear()

    if await cache.get(f'user_exists:{message.from_user.id}', int):
        message = await message.answer(
            'Добро пожаловать, {first_name} {last_name}! 😊 '
            'Нажмите на кнопку, чтобы войти в аккаунт 👇'.format(
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name),
            reply_markup=LOGIN_KB)
        await state.set_state(LoginGroup.waiting_for_click)
    else:
        message = await message.answer(
            'Добро пожаловать! Я бот, который помогает управлять паролями быстро и безопасно! 😊'
            'Давайте создадим аккаунт, для этого нажмите на кнопку 👇',
            reply_markup=REG_KB)
        await state.set_state(RegisterGroup.waiting_for_click)

    return message


@router.message(Command('suggest'))
async def suggest(message: types.Message, arq_redis: ArqRedis) -> Message:
    password = generate_password()
    sent_msg = await message.answer(
        f'Ваш случайный надёжный пароль:\n\n<code>{password}</code>'
    )
    await arq_redis.enqueue_job(
        'delete_message',
        _defer_by=timedelta(minutes=1),
        chat_id=message.from_user.id,
        message_id=sent_msg.message_id,
    )
    return sent_msg


@router.message(Command('help'))
async def help_(message: types.Message) -> Message:
    return await message.answer('<b>Способности бота:</b>\n\n' + BOT_COMMANDS_STR)


@router.message(Command('author'))
async def author(message: types.Message) -> Message:
    return await message.answer('Разработчик бота: @ivanstasevich 👨‍💻')
