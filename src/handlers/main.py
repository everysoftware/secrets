from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext

from src.db import Database
from src.db.models import Record
from src.encryption import encrypt_data, decrypt_data, generate_password
from src.fsm import MainGroup
from src.keyboards import get_main_kb, get_storage_kb
from src.middlewares import RegisterCheck
from .additional import update_last_msg, edit_last_msg, delete_last_msg
from .confirmation import confirm_master
from .redirects import redirects

main_router = Router(name='main')
main_router.message.middleware(RegisterCheck())
main_router.callback_query.middleware(RegisterCheck())


@main_router.message(MainGroup.main_menu)
@main_router.message(MainGroup.records_step)
async def main_menu(msg: types.Message, state: FSMContext, db: Database) -> None:
    match msg.text:
        case 'Хранилище 📁':
            await show_storage(msg, state, db)
        case 'Добавить ➕':
            await confirm_master(msg, state, add_record)
        case 'Сгенерировать 🔑':
            await gen_password(msg)
        case _:
            pass


@redirects.register_redirect
async def add_record(msg: types.Message, state: FSMContext) -> None:
    sent_msg = await msg.answer('Напечатай адрес сайта ⬇️')
    await update_last_msg(sent_msg, state)
    await state.set_state(MainGroup.address_step)


async def gen_password(msg: types.Message) -> None:
    password = generate_password()
    await msg.answer(
        f'🔑 Твой сгенерированный пароль:\n\n<code>{password}</code>',
    )


@main_router.message(MainGroup.address_step)
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
    await state.set_state(MainGroup.title_step)


@main_router.message(MainGroup.title_step)
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
    await state.set_state(MainGroup.username_step)


@main_router.message(MainGroup.username_step)
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
    await state.set_state(MainGroup.password_step)


@main_router.message(MainGroup.password_step)
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
        comment = db.comment.new(text='')
        db.record.new(
            user,
            user_data['url'],
            user_data['title'],
            username,
            password,
            salt,
            comment
        )

    await delete_last_msg(bot, user_data)
    await msg.answer(
        'Запись успешно добавлена в хранилище! ✅',
        reply_markup=get_main_kb()
    )
    await state.clear()
    await state.set_state(MainGroup.main_menu)


async def show_storage(msg: types.Message, state: FSMContext, db: Database) -> None:
    kb = await get_storage_kb(msg, db)
    sent_msg = await msg.answer(
        '<b>Записи хранилища</b>',
        reply_markup=kb
    )
    await update_last_msg(sent_msg, state)
    await state.set_state(MainGroup.records_step)


@main_router.callback_query(F.data.startswith('show'), MainGroup.records_step)
async def show_record_confirmation(callback: types.CallbackQuery, state: FSMContext) -> None:
    args = callback.data.split('_')
    try:
        record_id = int(args[1])
    except (IndexError, ValueError):
        pass
    else:
        await state.update_data(record_id=record_id)
        await confirm_master(callback.message, state, show_record)
    finally:
        await callback.answer()


@redirects.register_redirect
async def show_record(msg: types.Message, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        record: Record = await db.record.get(user_data['record_id'])
        username = decrypt_data(record.username, user_data['master'], record.salt)
        password = decrypt_data(record.password_, user_data['master'], record.salt)

        await msg.answer(
            f'<b>{record.title}</b>\n\n'
            f'🔗 Адрес сайта: {record.url}\n'
            f'👨 Имя пользователя: <code>{username}</code>\n'
            f'🔑 Пароль: <code>{password}</code>\n'
            f'💬 Комментарий:\n<tg-spoiler>{record.comment.text}</tg-spoiler>\n'
        )

    await state.clear()
    await state.set_state(MainGroup.records_step)
