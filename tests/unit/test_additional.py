import pytest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from bot.handlers.additional import update_last_message
from utils.entities import get_message, get_user, get_chat


@pytest.mark.asyncio
async def test_update_last_msg(storage, bot):
    msg, user, chat = get_message(), get_user(), get_chat()
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=user.id, chat_id=chat.id)
    )

    await update_last_message(state, msg)
    user_data = await state.get_data()

    assert user_data['chat_id'] == msg.chat.id
    assert user_data['last_msg_id'] == msg.message_id
    assert user_data['last_msg_text'] == msg.text
