from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import joinedload

from src.bot.fsm import LoginGroup
from src.bot.logic.main import show_main_menu
from src.bot.utils.security import DataVerification
from src.db import Database
from src.db.models import User

router = Router()


@router.message(LoginGroup.type_password)
async def authorize_user(message: types.Message, state: FSMContext, db: Database) -> None:
    async with db.session.begin():
        user = await db.user.get(message.from_user.id, options=[joinedload(User.auth_data)])

    await message.delete()

    if DataVerification.verify(message.text, user.auth_data.account_password, user.auth_data.salt):
        await message.answer('Авторизация прошла успешно ✅')
        await show_main_menu(message, state)
    else:
        await message.answer('Неверный пароль. Попробуйте ещё раз ⬇️')
