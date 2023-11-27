from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import joinedload

from src.bot.encryption import DataVerification
from src.bot.fsm import LoginGroup
from src.bot.handlers.activities import AuthorizeActivity
from src.bot.handlers.main import show_main_menu
from src.db import Database
from src.db.models import User

router = Router()


@router.message(F.text == 'Авторизация ⚡️', LoginGroup.in_lobby)
async def type_password(message: types.Message, state: FSMContext) -> None:
    await AuthorizeActivity.start(
        message, state, LoginGroup.typing_password,
        text='Введите пароль ⬇️'
    )


@router.message(LoginGroup.typing_password)
async def authorize_user(message: types.Message, state: FSMContext, db: Database) -> None:
    async with db.session.begin():
        user = await db.user.get(message.from_user.id, options=[joinedload(User.auth_data)])

    if DataVerification.verify(message.text, user.auth_data.account_password, user.auth_data.salt):
        await AuthorizeActivity.finish(
            message, state,
            text='Успешная авторизация ✅'
        )

        await show_main_menu(message, state)
    else:
        await AuthorizeActivity.switch(
            message, state,
            text='Неверный пароль. Попробуйте ещё раз ⬇️'
        )
