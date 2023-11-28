from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup, AddRecordGroup
from src.bot.fsm import RecordGroup
from src.bot.handlers.main import show_main_menu
from src.bot.handlers.user.verify_id import id_verification_request
from src.bot.security import Encryption
from src.bot.utils.callback_manager import manager
from src.db import Database
from src.db.models import Record

router = Router()


@router.message(MainGroup.viewing_main_menu, F.text == 'Добавить ⏬')
@router.message(MainGroup.viewing_all_records, F.text == 'Добавить ⏬')
@router.message(RecordGroup.viewing_record, F.text == 'Добавить ⏬')
async def add_record_request(message: types.Message, state: FSMContext) -> None:
    await id_verification_request(message, state, type_title, save_master=True)


@manager.callback
async def type_title(message: types.Message, state: FSMContext) -> None:
    await message.answer('Введите имя пароля ⬇️ Например, "Google"')
    await state.set_state(AddRecordGroup.typing_title)


@router.message(AddRecordGroup.typing_title, lambda message: len(message.text) > 64)
@router.message(AddRecordGroup.typing_username, lambda message: len(message.text) > 64)
@router.message(AddRecordGroup.typing_password, lambda message: len(message.text) > 64)
async def message_too_long(message: types.Message) -> None:
    await message.delete()
    await message.answer('Слишком длинное сообщение. Попробуйте ещё раз ⬇️')


@router.message(AddRecordGroup.typing_title, lambda message: len(message.text) <= 64)
async def type_username(message: types.Message, state: FSMContext) -> None:
    await message.delete()
    await state.update_data(title=message.text)
    await message.answer('Введите имя пользователя ⬇️ Например, "admin"')
    await state.set_state(AddRecordGroup.typing_username)


@router.message(AddRecordGroup.typing_username, lambda message: len(message.text) <= 64)
async def type_password(message: types.Message, state: FSMContext) -> None:
    await message.delete()
    await state.update_data(username=message.text)
    await message.answer('Введите пароль ⬇️ Например, "qwerty123"')
    await state.set_state(AddRecordGroup.typing_password)


@router.message(AddRecordGroup.typing_password, lambda message: len(message.text) <= 64)
async def add_record(message: types.Message, state: FSMContext, db: Database) -> None:
    await message.delete()

    user_data = await state.get_data()
    salt = Encryption.generate_salt()
    username = Encryption.encrypt(user_data['username'], user_data['master'], salt)
    password = Encryption.encrypt(message.text, user_data['master'], salt)

    async with db.session.begin():
        user = await db.user.get(message.from_user.id)
        db.record.new(Record(
            user=user,
            title=user_data['title'],
            username=username,
            password_=password,
            salt=salt
        ))

    await state.clear()
    await message.answer('Пароль успешно добавлен! ✅')
    await show_main_menu(message, state)
