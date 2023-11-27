from datetime import timedelta
from html import escape

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from arq import ArqRedis

from src.bot.fsm import LoginGroup, RegisterGroup
from src.bot.keyboards.auth import LOGIN_KB, REG_KB
from src.db import Database
from src.db.enums import UserRole
from src.db.models import User
from .commands import BOT_COMMANDS_STR
from ..security import generate_password
from ..middlewares import DatabaseMd

router = Router()

router.message.middleware(DatabaseMd())


@router.message(Command('start'))
async def start(
        message: types.Message,
        state: FSMContext,
        db: Database
) -> Message:
    async with db.session.begin():
        user = await db.user.get(message.from_user.id)

        if user is None:
            user = db.user.new(User(
                id=message.from_user.id,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
                language_code=message.from_user.language_code,
            ))

    match user.role:
        case UserRole.GUEST:
            message = await message.answer(
                'Добро пожаловать! Я бот, который помогает быстро и безопасно управлять паролями! 😊 '
                'Давайте создадим аккаунт, для этого нажмите на кнопку 👇',
                reply_markup=REG_KB)
            await state.set_state(RegisterGroup.in_lobby)
        case UserRole.USER:
            message = await message.answer(
                f'Добро пожаловать, {user.first_name} {user.last_name}! 😊 '
                f'Нажмите на кнопку, чтобы войти в аккаунт 👇',
                reply_markup=LOGIN_KB)
            await state.set_state(LoginGroup.in_lobby)
        case UserRole.ADMIN:
            message = await message.answer(
                f'Добро пожаловать, {user.first_name} {user.last_name}! 😊 '
                f'Вы администратор! 👨‍💻 Нажмите на кнопку, чтобы войти в аккаунт 👇')
        case _:
            raise ValueError(f'Unknown user role: {user.role}')

    return message


@router.message(Command('suggest'))
async def suggest(message: types.Message, arq_redis: ArqRedis) -> Message:
    password = generate_password()
    sent_msg = await message.answer(
        f'Ваш случайный пароль:\n\n<code>{escape(password)}</code>'
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


@router.message(Command('about'))
async def author(message: types.Message) -> Message:
    return await message.answer('👨‍💻 @ivanstasevich')
