from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.encryption import encrypt_data
from src.bot.fsm import MainGroup, RecordActionsGroup, RecordEditingGroup
from src.bot.keyboards import UPDATE_RECORD_KB
from src.bot.utils.messages import Interactive
from src.db import Database
from src.db.models import Comment

router = Router(name='record_editing')


@router.callback_query(F.data == 'edit_record', MainGroup.viewing_record)
async def edit_record(call: types.CallbackQuery, state: FSMContext) -> None:
    sent_msg = await call.message.answer(
        'Выбери элемент, который хочешь изменить в записи 🔽',
        reply_markup=UPDATE_RECORD_KB
    )
    await state.update_data(record_editing_message_id=sent_msg.message_id)
    await state.set_state(RecordActionsGroup.editing_record)

    await call.answer()


@router.callback_query(F.data == 'update_title', RecordActionsGroup.editing_record)
async def type_title(call: types.CallbackQuery, state: FSMContext) -> None:
    await Interactive.start(
        call.message, state,
        new_state=RecordEditingGroup.updating_title,
        text='Введи новое имя сайта ⬇️'
    )

    await call.answer()


@router.message(RecordEditingGroup.updating_title)
async def update_title(message: types.Message, state: FSMContext, db: Database) -> None:
    text = message.text.strip()
    user_data = await state.get_data()

    if len(text) > 64:
        return await Interactive.switch(
            message, state,
            user_data=user_data,
            text='Имя веб-сайта не может быть длиннее 64 символов. Введи новое имя сайта ⬇️',
        )

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.title = text
        await db.record.merge(record)

    await message.chat.delete_message(user_data['record_editing_message_id'])

    await Interactive.finish(
        message, state,
        user_data=user_data,
        new_state=MainGroup.viewing_record,
        text='Запись успешно изменена ✅',
        state_clear=False
    )


@router.callback_query(F.data == 'update_username', RecordActionsGroup.editing_record)
async def type_username(call: types.CallbackQuery, state: FSMContext) -> None:
    await Interactive.start(
        call.message, state,
        new_state=RecordEditingGroup.updating_username,
        text='Введи новое имя пользователя ⬇️'
    )

    await call.answer()


@router.message(RecordEditingGroup.updating_username)
async def update_username(message: types.Message, state: FSMContext, db: Database) -> None:
    text = message.text.strip()
    user_data = await state.get_data()

    if len(text) > 64:
        return await Interactive.switch(
            message, state,
            user_data=user_data,
            text='Имя пользователя не может быть длиннее 64 символов. Введи новое имя пользователя ⬇️',
        )

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.username = encrypt_data(text, user_data['master'], record.salt)[0]
        await db.record.merge(record)

    await message.chat.delete_message(user_data['record_editing_message_id'])

    await Interactive.finish(
        message, state,
        user_data=user_data,
        new_state=MainGroup.viewing_record,
        text='Запись успешно изменена ✅',
        state_clear=False
    )


@router.callback_query(F.data == 'update_password', RecordActionsGroup.editing_record)
async def type_password(call: types.CallbackQuery, state: FSMContext) -> None:
    await Interactive.start(
        call.message, state,
        new_state=RecordEditingGroup.updating_password,
        text='Введи новый пароль ⬇️'
    )

    await call.answer()


@router.message(RecordEditingGroup.updating_password)
async def update_password(message: types.Message, state: FSMContext, db: Database) -> None:
    text = message.text.strip()
    user_data = await state.get_data()

    if len(text) > 64:
        return await Interactive.switch(
            message, state,
            user_data=user_data,
            text='Пароль не может быть длиннее 64 символов. Введи новый пароль ⬇️',
        )

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.password_ = encrypt_data(text, user_data['master'], record.salt)[0]
        await db.record.merge(record)

    await message.chat.delete_message(user_data['record_editing_message_id'])

    await Interactive.finish(
        message, state,
        user_data=user_data,
        new_state=MainGroup.viewing_record,
        text='Запись успешно изменена ✅',
        state_clear=False
    )


@router.callback_query(F.data == 'update_url', RecordActionsGroup.editing_record)
async def type_url(call: types.CallbackQuery, state: FSMContext) -> None:
    await Interactive.start(
        call.message, state,
        new_state=RecordEditingGroup.updating_url,
        text='Введи новый веб-сайт ⬇️'
    )

    await call.answer()


@router.message(RecordEditingGroup.updating_url)
async def update_url(message: types.Message, state: FSMContext, db: Database) -> None:
    text = message.text.strip()
    user_data = await state.get_data()

    if len(text) > 64:
        return await Interactive.switch(
            message, state,
            user_data=user_data,
            text='Веб-сайт не может быть длиннее 64 символов. Введи новый веб-сайт ⬇️'
        )

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.url = text
        await db.record.merge(record)

    await message.chat.delete_message(user_data['record_editing_message_id'])

    await Interactive.finish(
        message, state,
        user_data=user_data,
        new_state=MainGroup.viewing_record,
        text='Запись успешно изменена ✅',
        state_clear=False
    )


@router.callback_query(F.data == 'update_comment', RecordActionsGroup.editing_record)
async def type_comment(call: types.CallbackQuery, state: FSMContext) -> None:
    await Interactive.start(
        call.message, state,
        new_state=RecordEditingGroup.updating_comment,
        text='Введи новый комментарий ⬇️'
    )

    await call.answer()


@router.message(RecordEditingGroup.updating_comment)
async def update_comment(message: types.Message, state: FSMContext, db: Database) -> None:
    text = message.text.strip()
    user_data = await state.get_data()

    if len(text) > 256:
        return await Interactive.switch(
            message, state,
            user_data=user_data,
            text='Комментарий не может быть длиннее 256 символов. Введи новый комментарий ⬇️'
        )

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])

        if record.comment is None:
            record.comment = db.comment.new(text=text)
            await db.record.merge(record)
        else:
            comment: Comment = record.comment
            comment.text = text
            await db.comment.merge(comment)

    await message.chat.delete_message(user_data['record_editing_message_id'])

    await Interactive.finish(
        message, state,
        user_data=user_data,
        new_state=MainGroup.viewing_record,
        text='Запись успешно изменена ✅',
        state_clear=False
    )
