from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext

from src.bot.handlers.additional import update_last_message, edit_last_message, delete_last_message
from src.bot.encryption import encrypt_data
from src.bot.filters import RegisterFilter
from src.bot.handlers.confirmation import confirm_master
from src.bot.handlers.forwarding import redirects
from src.bot.middlewares import DatabaseMd
from src.bot.structures.fsm import MainGroup, RecordActionsGroup, RecordEditingGroup
from src.bot.structures.keyboards import UPDATE_RECORD_KB
from src.db import Database
from src.db.models import Comment

router = Router(name='record_editing')

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

router.message.filter(RegisterFilter())
router.callback_query.filter(RegisterFilter())


@router.callback_query(F.data == 'edit_record', MainGroup.viewing_record)
async def edit_record_confirmation(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(RecordActionsGroup.editing_record)
    await confirm_master(callback.message, state, edit_record, True)
    await callback.answer()


@redirects.register_redirect
async def edit_record(msg: types.Message, state: FSMContext) -> None:
    sent_msg = await msg.answer(
        'Выбери элемент, который хочешь изменить в записи 🔽',
        reply_markup=UPDATE_RECORD_KB
    )
    await state.update_data(edit_record_msg_id=sent_msg.message_id)


@router.callback_query(F.data == 'update_title', RecordActionsGroup.editing_record)
async def type_title(callback: types.CallbackQuery, state: FSMContext) -> None:
    sent_msg = await callback.message.answer('Введи новое имя сайта ⬇️')
    await update_last_message(state, sent_msg)
    await state.set_state(RecordEditingGroup.updating_title)
    await callback.answer()


@router.callback_query(F.data == 'update_username', RecordActionsGroup.editing_record)
async def type_username(callback: types.CallbackQuery, state: FSMContext) -> None:
    sent_msg = await callback.message.answer('Введи новое имя пользователя ⬇️')
    await update_last_message(state, sent_msg)
    await state.set_state(RecordEditingGroup.updating_username)
    await callback.answer()


@router.callback_query(F.data == 'update_password', RecordActionsGroup.editing_record)
async def type_password(callback: types.CallbackQuery, state: FSMContext) -> None:
    sent_msg = await callback.message.answer('Введи новый пароль ⬇️')
    await update_last_message(state, sent_msg)
    await state.set_state(RecordEditingGroup.updating_password)
    await callback.answer()


@router.callback_query(F.data == 'update_url', RecordActionsGroup.editing_record)
async def type_url(callback: types.CallbackQuery, state: FSMContext) -> None:
    sent_msg = await callback.message.answer('Введи новый веб-сайт ⬇️')
    await update_last_message(state, sent_msg)
    await state.set_state(RecordEditingGroup.updating_url)
    await callback.answer()


@router.callback_query(F.data == 'update_comment', RecordActionsGroup.editing_record)
async def type_comment(callback: types.CallbackQuery, state: FSMContext) -> None:
    sent_msg = await callback.message.answer('Введи новый комментарий ⬇️')
    await update_last_message(state, sent_msg)
    await state.set_state(RecordEditingGroup.updating_comment)
    await callback.answer()


@router.message(RecordEditingGroup.updating_title)
async def update_title(msg: types.Message, state: FSMContext, db: Database, bot: Bot) -> None:
    text = msg.text.strip()
    user_data = await state.get_data()

    await msg.delete()

    if len(text) > 64:
        await edit_last_message(bot, state, user_data,
                                'Имя веб-сайта не может быть длиннее 64 символов. Введи новое имя сайта ⬇️')
        return

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.title = text
        await db.record.merge(record)

    await delete_last_message(bot, user_data)
    await msg.chat.delete_message(user_data['edit_record_msg_id'])

    await msg.answer('Запись успешно изменена ✅')
    await state.set_state(MainGroup.viewing_record)


@router.message(RecordEditingGroup.updating_username)
async def update_username(msg: types.Message, state: FSMContext, db: Database, bot: Bot) -> None:
    text = msg.text.strip()
    user_data = await state.get_data()

    await msg.delete()

    if len(text) > 64:
        await edit_last_message(bot, state, user_data,
                                'Имя пользователя не может быть длиннее 64 символов. Введи новое имя пользователя ⬇️')
        return

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.username = encrypt_data(text, user_data['master'], record.salt)[0]
        await db.record.merge(record)

    await delete_last_message(bot, user_data)
    await msg.chat.delete_message(user_data['edit_record_msg_id'])

    await msg.answer('Запись успешно изменена ✅')
    await state.set_state(MainGroup.viewing_record)


@router.message(RecordEditingGroup.updating_password)
async def update_password(msg: types.Message, state: FSMContext, db: Database, bot: Bot) -> None:
    text = msg.text.strip()
    user_data = await state.get_data()

    await msg.delete()

    if len(text) > 64:
        await edit_last_message(bot, state, user_data,
                                'Пароль не может быть длиннее 64 символов. Введи новый пароль ⬇️')
        return

    user_data = await state.get_data()
    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.password_ = encrypt_data(text, user_data['master'], record.salt)[0]
        await db.record.merge(record)

    await delete_last_message(bot, user_data)
    await msg.chat.delete_message(user_data['edit_record_msg_id'])

    await msg.answer('Запись успешно изменена ✅')
    await state.set_state(MainGroup.viewing_record)


@router.message(RecordEditingGroup.updating_url)
async def update_url(msg: types.Message, state: FSMContext, db: Database, bot: Bot) -> None:
    user_data = await state.get_data()
    text = msg.text.strip()

    await msg.delete()

    if len(text) > 64:
        await edit_last_message(bot, state, user_data,
                                'Веб-сайт не может быть длиннее 64 символов. Введи новый веб-сайт ⬇️')
        return

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])
        record.url = text
        await db.record.merge(record)

    await delete_last_message(bot, user_data)
    await msg.chat.delete_message(user_data['edit_record_msg_id'])

    await msg.answer('Запись успешно изменена ✅')
    await state.set_state(MainGroup.viewing_record)


@router.message(RecordEditingGroup.updating_comment)
async def update_comment(msg: types.Message, state: FSMContext, db: Database, bot: Bot) -> None:
    user_data = await state.get_data()
    text = msg.text.strip()

    await msg.delete()

    if len(text) > 256:
        await edit_last_message(bot, state, user_data,
                                'Комментарий не может быть длиннее 256 символов. Введи новый комментарий ⬇️')
        return

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'])

        if record.comment is None:
            record.comment = db.comment.new(text=text)
            await db.record.merge(record)
        else:
            comment: Comment = record.comment
            comment.text = text
            await db.comment.merge(comment)

    await delete_last_message(bot, user_data)

    await msg.chat.delete_message(user_data['edit_record_msg_id'])
    await msg.answer('Запись успешно изменена ✅')

    await state.set_state(MainGroup.viewing_record)
