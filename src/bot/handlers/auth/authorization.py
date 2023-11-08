from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from src.bot.fsm import LoginGroup
from src.bot.handlers.activities import AuthorizeActivity
from src.bot.handlers.main import show_main_menu
from src.db import Database

router = Router(name='authorization')


@router.message(F.text == 'Авторизация ⚡️', LoginGroup.waiting_for_click)
async def type_password(message: types.Message, state: FSMContext) -> None:
    await AuthorizeActivity.start(
        message, state, LoginGroup.typing_password,
        text='Введи пароль ⬇️'
    )


@router.message(LoginGroup.typing_password)
async def authorize_user(message: types.Message, state: FSMContext, db: Database) -> None:
    async with db.session.begin():
        result = await db.user.authorize(message.from_user.id, message.text)

    if result:
        await AuthorizeActivity.finish(
            message, state,
            text='Успешная авторизация ✅'
        )

        await show_main_menu(message, state)
    else:
        await AuthorizeActivity.switch(
            message, state,
            text='Неверный пароль. Попробуй ещё раз ⬇️'
        )
