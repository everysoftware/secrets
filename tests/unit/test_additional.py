import pytest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from bot.security import DataVerification
from src.bot.utils.messages import Activity
from utils.entities import get_message, get_user, get_chat


@pytest.mark.asyncio
async def test_activity_update_info(storage, bot):
    msg, user, chat = get_message(), get_user(), get_chat()
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=user.id, chat_id=chat.id)
    )

    await Activity.update_info(state, msg)
    user_data = await state.get_data()

    assert await Activity.message_id(user_data=user_data) == msg.message_id
    assert DataVerification.verify(msg.text, await Activity.message_hash(user_data=user_data))
