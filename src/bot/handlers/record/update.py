from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import joinedload

from src.bot.fsm import RecordGroup, UpdateRecordGroup
from src.bot.keyboards.record import UPDATE_RECORD_KB
from src.bot.security import Encryption
from src.db import Database
from src.db.models import Comment
from src.db.models import Record

router = Router()


@router.callback_query(F.data == 'update_record', RecordGroup.viewing_record)
async def update_record_question(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        'Выберите элемент, который Вы хотите изменить в записи 🔽',
        reply_markup=UPDATE_RECORD_KB
    )
    await state.set_state(RecordGroup.editing_record)
    await call.answer()


@router.callback_query(F.data == 'update_title', RecordGroup.editing_record)
async def type_title(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer('Введите новое имя пароля ⬇️')
    await state.set_state(UpdateRecordGroup.typing_title)
    await call.answer()


@router.message(UpdateRecordGroup.typing_title, lambda message: len(message.text) > 64)
@router.message(UpdateRecordGroup.typing_username, lambda message: len(message.text) > 64)
@router.message(UpdateRecordGroup.typing_password, lambda message: len(message.text) > 64)
@router.message(UpdateRecordGroup.typing_url, lambda message: len(message.text) > 64)
@router.message(UpdateRecordGroup.typing_comment, lambda message: len(message.text) > 256)
async def message_too_long(message: types.Message) -> None:
    await message.delete()
    await message.answer('Слишком длинное сообщение. Попробуйте ещё раз ⬇️')


@router.message(UpdateRecordGroup.typing_title, lambda message: len(message.text) <= 64)
async def update_title(message: types.Message, state: FSMContext, db: Database) -> None:
    await message.delete()
    user_data = await state.get_data()

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.title = message.text.strip()
        await db.record.merge(record)

    await message.answer('Запись успешно изменена ✅')
    await state.set_state(RecordGroup.editing_record)


@router.callback_query(F.data == 'update_username', RecordGroup.editing_record)
async def type_username(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer('Введите новое имя пользователя ⬇️ Например, "admin"')
    await state.set_state(UpdateRecordGroup.typing_username)
    await call.answer()


@router.message(UpdateRecordGroup.typing_username, lambda message: len(message.text) <= 64)
async def update_username(message: types.Message, state: FSMContext, db: Database) -> None:
    await message.delete()
    user_data = await state.get_data()

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.username = Encryption.encrypt(message.text, user_data['master'], record.salt)
        await db.record.merge(record)

    await message.answer('Запись успешно изменена ✅')
    await state.set_state(RecordGroup.editing_record)


@router.callback_query(F.data == 'update_password', RecordGroup.editing_record)
async def type_password(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer('Введите новый пароль ⬇️ Например, "qwerty123"')
    await state.set_state(UpdateRecordGroup.typing_password)
    await call.answer()


@router.message(UpdateRecordGroup.typing_password, lambda message: len(message.text) <= 64)
async def update_password(message: types.Message, state: FSMContext, db: Database) -> None:
    await message.delete()
    user_data = await state.get_data()

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.password_ = Encryption.encrypt(message.text, user_data['master'], record.salt)
        await db.record.merge(record)

    await message.answer('Запись успешно изменена ✅')
    await state.set_state(RecordGroup.editing_record)


@router.callback_query(F.data == 'update_url', RecordGroup.editing_record)
async def type_url(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer('Введите новый веб-сайт ⬇️ Например, "https://google.com"')
    await state.set_state(UpdateRecordGroup.typing_url)
    await call.answer()


@router.message(UpdateRecordGroup.typing_url, lambda message: len(message.text) <= 64)
async def update_url(message: types.Message, state: FSMContext, db: Database) -> None:
    await message.delete()
    user_data = await state.get_data()

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.url = message.text
        await db.record.merge(record)

    await message.answer('Запись успешно изменена ✅')
    await state.set_state(RecordGroup.editing_record)


@router.callback_query(F.data == 'update_comment', RecordGroup.editing_record)
async def type_comment(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer('Введите новый комментарий ⬇️ Например, "Это мой пароль от Google"')
    await state.set_state(UpdateRecordGroup.typing_comment)
    await call.answer()


@router.message(UpdateRecordGroup.typing_comment, lambda message: len(message.text) <= 256)
async def update_comment(message: types.Message, state: FSMContext, db: Database) -> None:
    await message.delete()
    user_data = await state.get_data()

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'], options=[joinedload(Record.comment)])

        if record.comment is None:
            record.comment = db.comment.new(Comment(text=message.text))
            await db.record.merge(record)
        else:
            comment: Comment = record.comment  # type: ignore
            comment.text = message.text
            await db.comment.merge(comment)

    await message.answer('Запись успешно изменена ✅')
    await state.set_state(RecordGroup.editing_record)


@router.callback_query(F.data == 'back', RecordGroup.editing_record)
async def back(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer('Вы вернулись в меню управления паролем 📝')
    await state.set_state(RecordGroup.viewing_record)
    await call.answer()
