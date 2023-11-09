from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.fsm import RegisterGroup
from src.bot.handlers.activities import RegisterActivity
from src.bot.handlers.main import show_main_menu
from src.db import Database

router = Router(name='register')


@router.message(F.text == 'Регистрация ⚡️', RegisterGroup.waiting_for_click)
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
        await db.user.register(
            db,
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language_code=message.from_user.language_code,
            password=user_data['password'],
            master=message.text,
        )

    await RegisterActivity.finish(
        message, state, user_data=user_data,
        text='Регистрация успешно завершена! ✅'
    )

    await show_main_menu(message, state)
