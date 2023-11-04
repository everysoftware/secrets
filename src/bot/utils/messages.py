from typing import Any, Optional

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply


class Interactive:

    @classmethod
    async def start(
            cls,
            message: types.Message,
            state: FSMContext,
            new_state: Optional[State] = None,
            text: Optional[str] = None,
            **kwargs
    ) -> None:
        sent_msg = await message.answer(text, **kwargs)
        await cls.update_info(state, sent_msg)

        if new_state is not None:
            await state.set_state(new_state)

    @classmethod
    async def update_info(
            cls,
            state: FSMContext,
            message: types.Message
    ) -> None:
        await state.update_data(
            chat_id=message.chat.id,
            last_msg_id=message.message_id,
            last_msg_text=message.text,
        )

    @classmethod
    async def switch(
            cls,
            message: types.Message,
            state: FSMContext,
            new_state: Optional[State] = None,
            user_data: Optional[dict[str, Any]] = None,
            text: Optional[str] = None,
            **kwargs,
    ) -> None:
        await message.delete()

        user_data = user_data or await state.get_data()

        if user_data['last_msg_text'] == text:
            return

        edited_msg = await message.bot.edit_message_text(
            text,
            user_data['chat_id'],
            user_data['last_msg_id'],
            **kwargs
        )

        await cls.update_info(state, edited_msg)

        if new_state is not None:
            await state.set_state(new_state)

    @classmethod
    async def delete(
            cls,
            message: types.Message,
            user_data: Optional[dict[str, Any]] = None,
            state: Optional[FSMContext] = None,
    ) -> None:
        if user_data is None and state is None:
            raise ValueError

        user_data = user_data or await state.get_data()

        await message.bot.delete_message(user_data['chat_id'], user_data['last_msg_id'])

    @classmethod
    async def finish(
            cls,
            message: types.Message,
            state: FSMContext,
            new_state: Optional[State] = None,
            user_data: Optional[dict[str, Any]] = None,
            state_clear: bool = True,
            text: Optional[str] = None,
            reply_markup: Optional[
                InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply] = None,
            **kwargs
    ) -> None:
        await cls.delete(message, state=state, user_data=user_data)
        await message.delete()

        if state_clear:
            await state.clear()

        await message.answer(text, reply_markup=reply_markup, **kwargs)

        if new_state is not None:
            await state.set_state(new_state)

    @classmethod
    async def finish_callback(
            cls,
            message: types.Message,
            state: FSMContext,
            new_state: Optional[State] = None,
            state_clear: bool = True,
            text: Optional[str] = None,
            reply_markup: Optional[
                InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply] = None,
            **kwargs
    ) -> None:
        await message.delete()

        if state_clear:
            await state.clear()

        await message.answer(text, reply_markup=reply_markup, **kwargs)

        if new_state is not None:
            await state.set_state(new_state)
