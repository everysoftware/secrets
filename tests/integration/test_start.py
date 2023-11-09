import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.methods import SendMessage
from aiogram.types import User
from sqlalchemy.orm import sessionmaker

from cache import Cache
from db import Database
from src.bot.keyboards.auth import LOGIN_KB, REG_KB
from utils.entities import get_update, get_message, get_user
from utils.mocked_bot import MockedBot


def get_users():
    users = [
        (True, get_user(id=123, first_name='Вася', last_name='Пупкин')),
        (False, get_user(id=418849724, first_name='Иван', last_name='Стасевич'))
    ]

    return users


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'is_registered, user',
    get_users()
)
async def test_start_command(
        is_registered: bool,
        user: User,
        dispatcher: Dispatcher,
        bot: MockedBot,
        db: Database,
        cache: Cache,
        pool: sessionmaker
) -> None:
    async with db.session.begin():
        if is_registered:
            await db.user.register(
                db,
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                language_code='ru-RU',
                password='test',
                master='test'
            )

    msg = get_message(text='/start', from_user=user)
    result = await dispatcher.feed_update(
        bot=bot,
        update=get_update(message=msg),
        cache=cache,
        pool=pool
    )

    assert isinstance(result, SendMessage)
    assert not is_registered and result.reply_markup == REG_KB or \
           is_registered and result.reply_markup == LOGIN_KB


@pytest.mark.asyncio
async def test_unknown_command(dispatcher: Dispatcher, bot: MockedBot, pool: sessionmaker):
    msg = get_message(text='/unknown')
    result = await dispatcher.feed_update(
        bot=bot,
        update=get_update(message=msg),
        pool=pool,
    )

    assert result is UNHANDLED
