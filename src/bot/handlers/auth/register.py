from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.security import DataVerification
from src.bot.fsm import RegisterGroup
from src.bot.handlers.activities import RegisterActivity
from src.bot.handlers.main import show_main_menu
from src.db import Database
from src.db.enums import UserRole
from src.db.models import AuthData

router = Router()


@router.message(F.text == 'Регистрация ⚡️', RegisterGroup.in_lobby)
async def type_password(message: types.Message, state: FSMContext) -> None:
    await RegisterActivity.start(
        message, state, RegisterGroup.typing_password,
        text='Придумайте надежный пароль ⬇️',
    )


@router.message(RegisterGroup.typing_password)
async def type_master(message: types.Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)
    await RegisterActivity.switch(
        message, state, RegisterGroup.typing_master,
        text='Придумайте надежный мастер-пароль ⬇️\n\n'
             '<b>Мастер-пароль даёт доступ ко всем вашим паролям. Никому не сообщаете его ❗️</b>'
    )


@router.message(RegisterGroup.typing_master)
async def register_user(
        message: types.Message,
        state: FSMContext,
        db: Database
) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        user = await db.user.get(message.from_user.id)
        salt = DataVerification.generate_salt()
        db.auth_data.new(AuthData(
            account_password=DataVerification.hash(user_data['password'], salt),
            master_password=DataVerification.hash(message.text, salt),
            salt=salt,
            user=user
        ))
        user.role = UserRole.USER

    await RegisterActivity.finish(
        message, state, user_data=user_data,
        text='Регистрация успешно завершена! ✅'
    )

    await show_main_menu(message, state)
