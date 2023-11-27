from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.security import Encryption
from src.bot.fsm import MainGroup, AddRecordGroup
from src.bot.fsm import RecordGroup
from src.bot.handlers.activities import AddRecordActivity
from src.bot.handlers.main import show_main_menu
from src.bot.handlers.user.confirm import id_verification_request
from src.bot.utils.callback_manager import manager
from src.db import Database
from src.db.models import Record

router = Router()


@router.message(MainGroup.viewing_main_menu, F.text == 'Добавить ⏬')
@router.message(MainGroup.viewing_all_records, F.text == 'Добавить ⏬')
@router.message(RecordGroup.viewing_record, F.text == 'Добавить ⏬')
async def add_record_request(message: types.Message, state: FSMContext) -> None:
    await id_verification_request(message, state, add_record, save_master=True)


@manager.callback
async def add_record(message: types.Message, state: FSMContext) -> None:
    await AddRecordActivity.start(
        message, state,
        new_state=AddRecordGroup.typing_title,
        text='Введите имя сайта ⬇️'
    )


@router.message(AddRecordGroup.typing_title)
async def set_title(message: types.Message, state: FSMContext) -> None:
    title = message.text.strip()

    if len(title) > 64:
        return await AddRecordActivity.switch(
            message, state,
            text='Имя сайта не может быть длиннее 64 символов. Введите имя сайта ⬇️'
        )

    await state.update_data(title=title)

    await AddRecordActivity.switch(
        message, state,
        new_state=AddRecordGroup.typing_username,
        text='Введите имя пользователя ⬇️'
    )


@router.message(AddRecordGroup.typing_username)
async def set_username(message: types.Message, state: FSMContext) -> None:
    username = message.text

    if len(username) > 64:
        return await AddRecordActivity.switch(
            message, state,
            text='Имя пользователя не может быть длиннее 64 символов. Введите имя пользователя ⬇️'
        )

    await state.update_data(username=username)

    await AddRecordActivity.switch(
        message, state,
        new_state=AddRecordGroup.typing_password,
        text='Введите пароль на сайте ⬇️'
    )


@router.message(AddRecordGroup.typing_password)
async def set_password(message: types.Message, state: FSMContext, db: Database) -> None:
    password = message.text
    user_data = await state.get_data()

    if len(password) > 64:
        return await AddRecordActivity.switch(
            message, state,
            user_data=user_data,
            text='Пароль не может быть длиннее 64 символов. Введите пароль на сайте ⬇️'
        )

    salt = Encryption.generate_salt()
    username = Encryption.encrypt(user_data['username'], user_data['master'], salt)
    password = Encryption.encrypt(password, user_data['master'], salt)

    async with db.session.begin():
        user = await db.user.get(message.from_user.id)
        db.record.new(Record(
            user=user,
            title=user_data['title'],
            username=username,
            password_=password,
            salt=salt
        ))

    await AddRecordActivity.finish(
        message, state,
        user_data=user_data,
        text='Пароль успешно добавлен! ✅'
    )

    await show_main_menu(message, state)
