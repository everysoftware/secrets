import pytest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from src.bot.utils.messages import Interactive
from utils.entities import get_message, get_user, get_chat


@pytest.mark.asyncio
async def test_interactive_update_info(storage, bot):
    msg, user, chat = get_message(), get_user(), get_chat()
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=user.id, chat_id=chat.id)
    )

    await Interactive.update_info(state, msg)
    user_data = await state.get_data()

    assert user_data['chat_id'] == msg.chat.id
    assert user_data['last_msg_id'] == msg.message_id
    assert user_data['last_msg_text'] == msg.text
