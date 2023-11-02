from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext

from src.bot.encryption import encrypt_data
from src.bot.filters import RegisterFilter
from src.bot.handlers.additional import update_last_message, edit_last_message, delete_last_message
from src.bot.handlers.confirmation import confirm_master
from src.bot.handlers.forwarding import redirects
from src.bot.middlewares import DatabaseMd
from src.bot.structures.fsm import MainGroup, RecordAdditionGroup
from src.bot.structures.keyboards import MAIN_MENU_KB
from src.db import Database

router = Router(name='record_addition')

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

router.message.filter(RegisterFilter())
router.callback_query.filter(RegisterFilter())


@router.message(MainGroup.viewing_main_menu, F.text == 'Добавить ⏬')
@router.message(MainGroup.viewing_storage, F.text == 'Добавить ⏬')
@router.message(MainGroup.viewing_record, F.text == 'Добавить ⏬')
async def add_record_confirmation(msg: types.Message, state: FSMContext) -> None:
    await confirm_master(msg, state, add_record, True)


@redirects.register_redirect
async def add_record(msg: types.Message, state: FSMContext) -> None:
    sent_msg = await msg.answer('Напечатай имя сайта ⬇️')
    await update_last_message(state, sent_msg)
    await state.set_state(RecordAdditionGroup.setting_title)


@router.message(RecordAdditionGroup.setting_title)
async def set_title(msg: types.Message, state: FSMContext, bot: Bot) -> None:
    title = msg.text.strip()
    await msg.delete()
    user_data = await state.get_data()

    if len(title) > 64:
        await edit_last_message(bot, state, user_data,
                                'Имя сайта не может быть длиннее 64 символов. Напечатай имя сайта ⬇️')
        return

    await state.update_data(title=title)
    await edit_last_message(bot, state, user_data, 'Напечатай имя пользователя на сайте ⬇️')
    await state.set_state(RecordAdditionGroup.setting_username)


@router.message(RecordAdditionGroup.setting_username)
async def set_username(msg: types.Message, state: FSMContext, bot: Bot) -> None:
    username = msg.text
    await msg.delete()
    user_data = await state.get_data()

    if len(username) > 64:
        await edit_last_message(
            bot, state, user_data,
            'Имя пользователя не может быть длиннее 64 символов. Напечатай имя пользователя на сайте ⬇️'
        )
        return

    await state.update_data(username=username)

    await edit_last_message(bot, state, user_data, 'Напечатай пароль на сайте ⬇️')
    await state.set_state(RecordAdditionGroup.setting_password)


@router.message(RecordAdditionGroup.setting_password)
async def set_password(msg: types.Message, state: FSMContext, db: Database, bot: Bot) -> None:
    password = msg.text
    await msg.delete()
    user_data = await state.get_data()

    if len(password) > 64:
        await edit_last_message(bot, state, user_data,
                                'Пароль не может быть длиннее 64 символов. Напечатай пароль на сайте ⬇️')
        return

    username, salt = encrypt_data(user_data['username'], user_data['master'])
    password, _ = encrypt_data(password, user_data['master'], salt)

    async with db.session.begin():
        user = await db.user.get(msg.from_user.id)
        db.record.new(
            user,
            user_data['title'],
            username,
            password,
            salt
        )

    await delete_last_message(bot, user_data)
    await msg.answer(
        'Запись успешно добавлена в хранилище! ✅',
        reply_markup=MAIN_MENU_KB
    )
    await state.clear()
    await state.set_state(MainGroup.viewing_main_menu)
