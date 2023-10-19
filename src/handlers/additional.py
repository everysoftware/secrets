from typing import Any

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext


async def update_last_msg(msg: types.Message, state: FSMContext) -> None:
    await state.update_data(
        chat_id=msg.chat.id,
        last_msg_id=msg.message_id,
        last_msg_text=msg.text,
    )


async def delete_last_msg(bot: Bot, user_data: dict[str, Any]) -> None:
    await bot.delete_message(user_data['chat_id'], user_data['last_msg_id'])


async def edit_last_msg(bot: Bot, user_data: dict[str, Any], state: FSMContext, text: str) -> None:
    if user_data['last_msg_text'] != text:
        await update_last_msg(
            await bot.edit_message_text(text, user_data['chat_id'], user_data['last_msg_id']),
            state
        )
