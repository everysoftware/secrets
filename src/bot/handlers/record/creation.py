from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.encryption import Encryption
from src.bot.fsm import MainGroup, RecordCreationGroup
from src.bot.handlers.user.confirmation import send_confirmation_request
from src.bot.keyboards import MAIN_MENU_KB
from src.bot.utils.forwarding import redirects
from src.bot.utils.messages import Interactive
from src.db import Database

router = Router(name='record_creation')


@router.message(MainGroup.viewing_main_menu, F.text == 'Добавить ⏬')
@router.message(MainGroup.viewing_storage, F.text == 'Добавить ⏬')
@router.message(MainGroup.viewing_record, F.text == 'Добавить ⏬')
async def add_record_confirmation(message: types.Message, state: FSMContext) -> None:
    await send_confirmation_request(message, state, add_record, save_master=True)


@redirects.register_redirect
async def add_record(message: types.Message, state: FSMContext) -> None:
    await Interactive.start(
        message, state,
        new_state=RecordCreationGroup.setting_title,
        text='Напечатай имя сайта ⬇️'
    )


@router.message(RecordCreationGroup.setting_title)
async def set_title(message: types.Message, state: FSMContext) -> None:
    title = message.text.strip()

    if len(title) > 64:
        return await Interactive.switch(
            message, state,
            text='Имя сайта не может быть длиннее 64 символов. Напечатай имя сайта ⬇️'
        )

    await state.update_data(title=title)

    await Interactive.switch(
        message, state,
        new_state=RecordCreationGroup.setting_username,
        text='Напечатай имя пользователя на сайте ⬇️'
    )


@router.message(RecordCreationGroup.setting_username)
async def set_username(message: types.Message, state: FSMContext) -> None:
    username = message.text

    if len(username) > 64:
        return await Interactive.switch(
            message, state,
            text='Имя пользователя не может быть длиннее 64 символов. Напечатай имя пользователя на сайте ⬇️'
        )

    await state.update_data(username=username)

    await Interactive.switch(
        message, state,
        new_state=RecordCreationGroup.setting_password,
        text='Напечатай пароль на сайте ⬇️'
    )


@router.message(RecordCreationGroup.setting_password)
async def set_password(message: types.Message, state: FSMContext, db: Database) -> None:
    password = message.text
    user_data = await state.get_data()

    if len(password) > 64:
        return await Interactive.switch(
            message, state,
            user_data=user_data,
            text='Пароль не может быть длиннее 64 символов. Напечатай пароль на сайте ⬇️'
        )

    salt = Encryption.generate_salt()
    username = Encryption.encrypt(user_data['username'], user_data['master'], salt)
    password = Encryption.encrypt(password, user_data['master'], salt)

    async with db.session.begin():
        user = await db.user.get(message.from_user.id)
        db.record.new(
            user,
            user_data['title'],
            username,
            password,
            salt
        )

    await Interactive.finish(
        message, state,
        new_state=MainGroup.viewing_main_menu,
        user_data=user_data,
        text='Запись успешно добавлена в хранилище! ✅',
        reply_markup=MAIN_MENU_KB
    )
