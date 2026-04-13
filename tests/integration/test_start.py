import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from sqlalchemy.orm import sessionmaker

from utils.tg_entities import get_update, get_message
from utils.mocked_bot import MockedBot


@pytest.mark.asyncio
async def test_unknown_command(dispatcher: Dispatcher, bot: MockedBot, pool: sessionmaker):
    msg = get_message(text='/unknown')
    result = await dispatcher.feed_update(
        bot=bot,
        update=get_update(message=msg),
        pool=pool,
    )

    assert result is UNHANDLED
