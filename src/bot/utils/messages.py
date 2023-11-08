from abc import ABC
from contextlib import suppress
from typing import Any, Optional

from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply

from src.bot.encryption import Verifying


class Activity(ABC):

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    @classmethod
    async def update_info(
            cls,
            state: FSMContext,
            message: types.Message
    ) -> None:
        await state.update_data(
            {
                f'activity:{cls.name()}:message_id': message.message_id,
                f'activity:{cls.name()}:message_hash': Verifying.get_hash(message.text)
            }
        )

    @classmethod
    async def message_id(
            cls,
            state: Optional[FSMContext] = None,
            user_data: Optional[dict[str, Any]] = None
    ) -> int:
        user_data = user_data or await state.get_data()

        return user_data[f'activity:{cls.name()}:message_id']

    @classmethod
    async def message_hash(
            cls,
            state: Optional[FSMContext] = None,
            user_data: Optional[dict[str, Any]] = None
    ) -> str:
        user_data = user_data or await state.get_data()

        return user_data[f'activity:{cls.name()}:message_hash']

    @classmethod
    async def start(
            cls,
            message: types.Message,
            state: FSMContext,
            new_state: Optional[State] = None,
            text: Optional[str] = None,
            reply_markup: Optional[
                InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply] = None
    ) -> types.Message:
        sent_msg = await message.answer(text, reply_markup=reply_markup)
        await cls.update_info(state, sent_msg)

        if new_state is not None:
            await state.set_state(new_state)

        return sent_msg

    @classmethod
    async def start_callback(
            cls,
            call: types.CallbackQuery,
            state: FSMContext,
            new_state: Optional[State] = None,
            text: Optional[str] = None,
            reply_markup: Optional[
                InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply] = None
    ) -> types.Message:
        sent_msg = await call.message.answer(text, reply_markup=reply_markup)
        await cls.update_info(state, sent_msg)

        if new_state is not None:
            await state.set_state(new_state)

        await call.answer()

        return sent_msg

    @classmethod
    async def switch(
            cls,
            message: types.Message,
            state: FSMContext,
            new_state: Optional[State] = None,
            user_data: Optional[dict[str, Any]] = None,
            text: Optional[str] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> None:
        await message.delete()

        user_data = user_data or await state.get_data()

        if Verifying.verify(text, await cls.message_hash(user_data=user_data)):
            return

        edited_msg = await message.bot.edit_message_text(
            text,
            message.chat.id,
            await cls.message_id(user_data=user_data),
            reply_markup=reply_markup
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

        with suppress(TelegramBadRequest):
            await message.bot.delete_message(
                message.chat.id,
                await cls.message_id(state=state)
            )

    @classmethod
    async def finish(
            cls,
            message: types.Message,
            state: FSMContext,
            new_state: Optional[State] = None,
            user_data: Optional[dict[str, Any]] = None,
            state_clear: bool = False,
            text: Optional[str] = None,
            reply_markup: Optional[
                InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply] = None
    ) -> None:
        await cls.delete(message, state=state, user_data=user_data)
        with suppress(TelegramBadRequest):
            await message.delete()

        if state_clear:
            await state.clear()

        if text:
            await message.answer(text, reply_markup=reply_markup)

        if new_state is not None:
            await state.set_state(new_state)

    @classmethod
    async def finish_callback(
            cls,
            call: types.CallbackQuery,
            state: FSMContext,
            new_state: Optional[State] = None,
            state_clear: bool = False,
            text: Optional[str] = None,
    ) -> None:
        with suppress(TelegramBadRequest):
            await call.message.delete()

        if state_clear:
            await state.clear()

        await call.answer(text)

        if new_state is not None:
            await state.set_state(new_state)
