from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from src.bot.fsm import RegisterGroup
from src.bot.logic.main import show_main_menu
from src.bot.utils.security import DataVerification
from src.db import Database
from src.db.enums import UserRole
from src.db.models import Credentials

router = Router()


@router.message(F.text == "Регистрация ⚡️", RegisterGroup.in_lobby)
async def type_password(message: types.Message, state: FSMContext) -> None:
    await message.answer("Введите пароль ⬇️")
    await state.set_state(RegisterGroup.type_password)


@router.message(RegisterGroup.type_password)
async def type_master(message: types.Message, state: FSMContext) -> None:
    await message.delete()
    await state.update_data(password=message.text)
    await message.answer(
        "Введите мастер-пароль ⬇️\n\n"
        "<b>Мастер-пароль позволяет вам управлять всеми вашими паролями. "
        "Не подвергайте опасности свои данные и не сообщайте его ни при каких обстоятельствах! ❗</b>"
    )
    await state.set_state(RegisterGroup.type_master)


@router.message(RegisterGroup.type_master)
async def register_user(
    message: types.Message, state: FSMContext, db: Database
) -> None:
    await message.delete()
    user_data = await state.get_data()

    async with db.session.begin():
        user = await db.user.get(message.from_user.id)
        salt = DataVerification.generate_salt()
        db.credentials.new(
            Credentials(
                password=DataVerification.hash(user_data["password"], salt),
                master_password=DataVerification.hash(message.text, salt),
                salt=salt,
                user=user,
            )
        )
        user.role = UserRole.USER

    await message.answer("Регистрация прошла успешно ✅")
    await show_main_menu(message, state)
