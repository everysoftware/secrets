from typing import Any, Awaitable, Callable

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from arq import ArqRedis
from sqlalchemy.orm import joinedload

from src.bot.fsm import EditRecordGroup, RecordGroup
from src.bot.keyboards.record import EDIT_RECORD_KB
from src.bot.logic.record.get import show_record
from src.bot.utils.security import Encryption
from src.db import Database
from src.db.models import Comment, Record

router = Router()


async def edit_record_question(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        "Выберите элемент, который Вы хотите изменить в записи 🔽",
        reply_markup=EDIT_RECORD_KB,
    )
    await state.set_state(RecordGroup.edit_record)


@router.callback_query(F.data == "edit_record", RecordGroup.view_record)
async def process_callback(call: types.CallbackQuery, state: FSMContext) -> None:
    await edit_record_question(call.message, state)
    await call.answer()


def make_type_handler(
    field_name, text: str, new_state: State
) -> Callable[..., Awaitable]:
    @router.callback_query(F.data == f"edit_{field_name}", RecordGroup.edit_record)
    async def type_handler(call: types.CallbackQuery, state: FSMContext) -> None:
        await call.message.answer(text)
        await state.set_state(new_state)
        await call.answer()

    return type_handler


def make_update_handler(
    field_name: str,
    *filters: Callable,
    encrypt: bool = False,
    callback: Callable[..., Awaitable] | None = None,
) -> Callable[..., Awaitable]:
    @router.message(*filters)
    async def handler(
        message: types.Message, state: FSMContext, db: Database, rq: ArqRedis
    ) -> None:
        await message.delete()
        user_data = await state.get_data()

        async with db.session.begin():
            if callback is not None:
                await callback(message, db, user_data)
            else:
                record = await db.record.get(user_data["record_id"])
                value = message.text
                if encrypt:
                    decrypted_value = Encryption.encrypt(
                        value, user_data["master"], record.salt
                    )
                setattr(record, field_name, decrypted_value)
                await db.record.merge(record)

        db.session.expunge_all()
        await message.answer("Запись успешно изменена ✅")
        await show_record(message, state, db, rq)

    return handler


def make_handlers(
    field_name: str,
    text: str,
    state: State,
    *filters: Callable,
    encrypt: bool = False,
    callback: Callable[..., Awaitable] | None = None,
) -> tuple[Callable[..., Awaitable], ...]:
    return (
        make_type_handler(field_name, text, state),
        make_update_handler(
            field_name, state, *filters, encrypt=encrypt, callback=callback
        ),
    )


make_handlers(
    "title",
    "Введите новое имя пароля ⬇️ Например, <code>Google</code>",
    EditRecordGroup.type_title,
    lambda message: len(message.text) <= 64,
)

make_handlers(
    "username",
    "Введите новое имя пользователя ⬇️ Например, <code>admin</code>",
    EditRecordGroup.type_username,
    lambda message: len(message.text) <= 64,
    encrypt=True,
)

make_handlers(
    "password",
    "Введите новый пароль ⬇️ Например, <code>qwerty123</code>",
    EditRecordGroup.type_password,
    lambda message: len(message.text) <= 64,
    encrypt=True,
)

make_handlers(
    "url",
    "Введите новый веб-сайт ⬇️ Например, <code>https://google.com</code>",
    EditRecordGroup.type_url,
    lambda message: len(message.text) <= 64,
)


async def edit_comment_callback(
    message: types.Message, db: Database, user_data: dict[str, Any]
) -> None:
    record = await db.record.get(
        user_data["record_id"], options=[joinedload(Record.comment)]
    )

    if record.comment is None:
        record.comment = db.comment.new(Comment(text=message.text))
        await db.record.merge(record)
    else:
        comment: Comment = record.comment  # type: ignore
        comment.text = message.text
        await db.comment.merge(comment)


make_handlers(
    "comment",
    "Введите новый комментарий ⬇️ Например, <code>Это мой пароль от Google</code>",
    EditRecordGroup.type_comment,
    lambda message: len(message.text) <= 256,
    callback=edit_comment_callback,
)


@router.message(*EditRecordGroup.__all_states__)
async def message_too_long(message: types.Message) -> None:
    await message.delete()
    await message.answer("Слишком длинное сообщение. Попробуйте ещё раз ⬇️")


@router.callback_query(F.data == "back", RecordGroup.edit_record)
async def back_to_record(
    call: types.CallbackQuery, state: FSMContext, db: Database, rq: ArqRedis
) -> None:
    await show_record(call, state, db, rq)
    await call.answer()
