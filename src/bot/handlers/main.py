from datetime import timedelta

from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext
from arq import ArqRedis

from src.bot.encryption import encrypt_data, decrypt_data, generate_password
from src.bot.filters import RegisterFilter
from src.bot.middlewares import DatabaseMd
from src.bot.structures.fsm import MainGroup
from src.bot.structures.keyboards import MAIN_MENU_KB, get_storage_kb, YESNO_KB, RECORD_KB
from src.db import Database
from src.db.models import Record
from .additional import update_last_msg, edit_last_msg, delete_last_msg
from .confirmation import confirm_master
from .redirects import redirects

main_router = Router(name='main')

main_router.message.middleware(DatabaseMd())
main_router.callback_query.middleware(DatabaseMd())

main_router.message.filter(RegisterFilter())
main_router.callback_query.filter(RegisterFilter())


async def show_main_menu(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(
        'Ты в главном меню бота. Для навигации используй кнопки внизу 👇',
        reply_markup=MAIN_MENU_KB
    )
    await state.set_state(MainGroup.viewing_main_menu)


@main_router.message(MainGroup.viewing_main_menu, F.text == 'Добавить ⏬')
@main_router.message(MainGroup.viewing_storage, F.text == 'Добавить ⏬')
@main_router.message(MainGroup.viewing_record, F.text == 'Добавить ⏬')
async def add_record_confirmation(msg: types.Message, state: FSMContext) -> None:
    await confirm_master(msg, state, add_record, True)


@redirects.register_redirect
async def add_record(msg: types.Message, state: FSMContext) -> None:
    sent_msg = await msg.answer('Напечатай адрес сайта ⬇️')
    await update_last_msg(sent_msg, state)
    await state.set_state(MainGroup.setting_url)


@main_router.message(MainGroup.viewing_main_menu, F.text == 'Сгенерировать 🔑')
@main_router.message(MainGroup.viewing_storage, F.text == 'Сгенерировать 🔑')
@main_router.message(MainGroup.viewing_record, F.text == 'Сгенерировать 🔑')
async def gen_password(msg: types.Message, arq_redis: ArqRedis) -> None:
    password = generate_password()
    sent_msg = await msg.answer(
        f'🔑 Твой сгенерированный пароль:\n\n<code>{password}</code>'
    )
    await arq_redis.enqueue_job(
        'delete_message',
        _defer_by=timedelta(minutes=1),
        chat_id=msg.from_user.id,
        message_id=sent_msg.message_id,
    )


@main_router.message(MainGroup.setting_url)
async def address_step(msg: types.Message, state: FSMContext, bot: Bot) -> None:
    url = msg.text.strip()
    await msg.delete()
    user_data = await state.get_data()

    if len(url) > 64:
        await edit_last_msg(bot, user_data, state,
                            'Адрес сайта не может быть длиннее 64 символов. Напечатай адрес сайта ⬇️')
        return

    await state.update_data(url=url)
    await edit_last_msg(bot, user_data, state, 'Напечатай заголовок, который будет отображаться в хранилище ⬇️\n\n'
                                               '<i>Ты можешь пропустить этот шаг. Для этого отправь 0, '
                                               'тогда в списке будет отображаться адрес сайта.</i>')
    await state.set_state(MainGroup.setting_title)


@main_router.message(MainGroup.setting_title)
async def title_step(msg: types.Message, state: FSMContext, bot: Bot) -> None:
    title = msg.text.strip()
    await msg.delete()
    user_data = await state.get_data()

    if len(title) > 64:
        await edit_last_msg(bot, user_data, state,
                            'Заголовок сайта не может быть длиннее 64 символов. Напечатай заголовок сайта ⬇️')
        return

    if title == '0':
        title = user_data['url']

    await state.update_data(title=title)
    await edit_last_msg(bot, user_data, state, 'Напечатай имя пользователя на сайте ⬇️')
    await state.set_state(MainGroup.setting_username)


@main_router.message(MainGroup.setting_username)
async def username_step(msg: types.Message, state: FSMContext, bot: Bot) -> None:
    username = msg.text
    await msg.delete()
    user_data = await state.get_data()

    if len(username) > 64:
        await edit_last_msg(
            bot, user_data, state,
            'Имя пользователя не может быть длиннее 64 символов. Напечатай имя пользователя на сайте ⬇️')
        return

    await state.update_data(username=username)

    await edit_last_msg(bot, user_data, state, 'Напечатай пароль на сайте ⬇️')
    await state.set_state(MainGroup.setting_password)


@main_router.message(MainGroup.setting_password)
async def password_step(msg: types.Message, state: FSMContext, db: Database, bot: Bot) -> None:
    password = msg.text
    await msg.delete()
    user_data = await state.get_data()

    if len(password) > 64:
        await edit_last_msg(bot, user_data, state,
                            'Пароль не может быть длиннее 64 символов. Напечатай пароль на сайте ⬇️')
        return

    username, salt = encrypt_data(user_data['username'], user_data['master'])
    password, _ = encrypt_data(password, user_data['master'], salt)

    async with db.session.begin():
        user = await db.user.get(msg.from_user.id)
        db.record.new(
            user,
            user_data['url'],
            user_data['title'],
            username,
            password,
            salt
        )

    await delete_last_msg(bot, user_data)
    await msg.answer(
        'Запись успешно добавлена в хранилище! ✅',
        reply_markup=MAIN_MENU_KB
    )
    await state.clear()
    await state.set_state(MainGroup.viewing_main_menu)


@main_router.message(MainGroup.viewing_main_menu, F.text == 'Хранилище 📁')
@main_router.message(MainGroup.viewing_storage, F.text == 'Хранилище 📁')
@main_router.message(MainGroup.viewing_record, F.text == 'Хранилище 📁')
async def show_storage(msg: types.Message, state: FSMContext, db: Database) -> None:
    kb = await get_storage_kb(msg, db)
    sent_msg = await msg.answer(
        '<b>Записи хранилища</b>',
        reply_markup=kb
    )
    await update_last_msg(sent_msg, state)
    await state.set_state(MainGroup.viewing_storage)


@main_router.callback_query(F.data.startswith('show_record'), MainGroup.viewing_storage)
@main_router.callback_query(F.data.startswith('show_record'), MainGroup.viewing_record)
async def show_record_confirmation(callback: types.CallbackQuery, state: FSMContext) -> None:
    args = callback.data.split('_')
    try:
        record_id = int(args[2])
    except (IndexError, ValueError):
        pass
    else:
        await state.update_data(record_id=record_id)
        await confirm_master(callback.message, state, show_record, True)
    finally:
        await callback.answer()


@redirects.register_redirect
async def show_record(msg: types.Message, state: FSMContext, db: Database, arq_redis: ArqRedis) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        record: Record = await db.record.get(user_data['record_id'])
        username = decrypt_data(record.username, user_data['master'], record.salt)
        password = decrypt_data(record.password_, user_data['master'], record.salt)
        comment = record.comment.text if record.comment else ''

        record_msg = await msg.answer(
            f'<b>{record.title}</b>\n\n'
            f'🔗 Адрес сайта: {record.url}\n'
            f'👨 Имя пользователя: <code>{username}</code>\n'
            f'🔑 Пароль: <code>{password}</code>\n'
            f'💬 Комментарий: <tg-spoiler>{comment}</tg-spoiler>\n\n'
        )

    cp_msg = await msg.answer(
        'Выбери действие',
        reply_markup=RECORD_KB
    )

    await arq_redis.enqueue_job(
        'delete_record_message',
        _defer_by=timedelta(minutes=2),
        chat_id=msg.from_user.id,
        record_msg_id=record_msg.message_id,
        cp_msg_id=cp_msg.message_id
    )

    await state.clear()

    await state.set_state(MainGroup.viewing_record)
    await state.update_data(record_id=user_data['record_id'])
    await state.update_data(record_msg_id=record_msg.message_id)


@main_router.callback_query(F.data == 'edit_record', MainGroup.viewing_record)
async def edit_record(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(MainGroup.editing_record)
    await callback.answer()


@main_router.callback_query(F.data == 'delete_record', MainGroup.viewing_record)
async def delete_record_confirmation(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(MainGroup.deleting_record)
    await confirm_master(callback.message, state, delete_record_yesno)
    await callback.answer()


@redirects.register_redirect
async def delete_record_yesno(msg: types.Message) -> None:
    await msg.answer(
        'После удаления записи её нельзя будет восстановить. Ты действительно хочешь удалить запись?',
        reply_markup=YESNO_KB
    )


@main_router.callback_query(F.data == 'yes', MainGroup.deleting_record)
async def delete_record_yes(callback: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        await db.record.delete(Record.id == user_data['record_id'])

    await callback.message.answer('Запись успешно удалена ✅')
    await state.set_state(MainGroup.viewing_storage)

    await callback.answer()


@main_router.callback_query(F.data == 'no', MainGroup.deleting_record)
async def delete_record_no(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer('Удаление записи отменено ❌')
    await state.set_state(MainGroup.viewing_record)

    await callback.answer()


@main_router.callback_query(F.data == 'delete_msg_record', MainGroup.viewing_record)
async def delete_record_msg(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()

    await callback.message.chat.delete_message(user_data['record_msg_id'])
    await callback.message.delete()

    await state.set_state(MainGroup.viewing_storage)

    await callback.answer()
