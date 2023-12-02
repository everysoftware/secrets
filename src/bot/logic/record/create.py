from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from src.bot.fsm import AddRecordGroup, MainGroup, RecordGroup
from src.bot.logic.main import show_main_menu
from src.bot.logic.user.verify_id import id_verification_request
from src.bot.utils.callback_manager import manager
from src.bot.utils.security import Encryption
from src.db import Database
from src.db.models import Record

router = Router()


@router.message(MainGroup.view_main_menu, F.text == "Добавить ⏬")
@router.message(MainGroup.view_all_records, F.text == "Добавить ⏬")
@router.message(RecordGroup.view_record, F.text == "Добавить ⏬")
@router.message(MainGroup.view_user, F.text == "Добавить ⏬")
async def add_record_request(message: types.Message, state: FSMContext) -> None:
    await id_verification_request(message, state, type_title, save_master=True)


@manager.callback
async def type_title(message: types.Message, state: FSMContext) -> None:
    await message.answer("Введите имя пароля ⬇️ Например, <code>Google</code>")
    await state.set_state(AddRecordGroup.type_title)


@router.message(AddRecordGroup.type_title, lambda message: len(message.text) > 64)
@router.message(AddRecordGroup.type_username, lambda message: len(message.text) > 64)
@router.message(AddRecordGroup.type_password, lambda message: len(message.text) > 64)
async def message_too_long(message: types.Message) -> None:
    await message.delete()
    await message.answer("Слишком длинное сообщение. Попробуйте ещё раз ⬇️")


@router.message(AddRecordGroup.type_title, lambda message: len(message.text) <= 64)
async def type_username(message: types.Message, state: FSMContext) -> None:
    await message.delete()
    await state.update_data(title=message.text)
    await message.answer("Введите имя пользователя ⬇️ Например, <code>admin</code>")
    await state.set_state(AddRecordGroup.type_username)


@router.message(AddRecordGroup.type_username, lambda message: len(message.text) <= 64)
async def type_password(message: types.Message, state: FSMContext) -> None:
    await message.delete()
    await state.update_data(username=message.text)
    await message.answer("Введите пароль ⬇️ Например, <code>qwerty123</code>")
    await state.set_state(AddRecordGroup.type_password)


@router.message(AddRecordGroup.type_password, lambda message: len(message.text) <= 64)
async def add_record(message: types.Message, state: FSMContext, db: Database) -> None:
    await message.delete()

    user_data = await state.get_data()
    salt = Encryption.generate_salt()
    username = Encryption.encrypt(user_data["username"], user_data["master"], salt)
    password = Encryption.encrypt(message.text, user_data["master"], salt)

    async with db.session.begin():
        user = await db.user.get(message.from_user.id)
        db.record.new(
            Record(
                user=user,
                title=user_data["title"],
                username=username,
                password=password,
                salt=salt,
            )
        )

    await state.clear()
    await message.answer("Пароль успешно добавлен! ✅")
    await show_main_menu(message, state)
