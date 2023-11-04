from typing import Callable

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.bot.fsm import LoginGroup
from src.bot.utils.forwarding import Redirects
from src.bot.utils.messages import Interactive
from src.db import Database

router = Router(name='confirmation')


async def send_confirmation_request(
        message: types.Message,
        state: FSMContext,
        redirect: Callable,
        save_master: bool = False
) -> None:
    await state.update_data(last_state=await state.get_state())
    await state.update_data(redirect=redirect.__name__)
    await state.update_data(save_master=save_master)

    await Interactive.start(
        message, state, LoginGroup.master_confirmation,
        text='Для подтверждения операции введите мастер-пароль ⬇️'
    )


@router.message(LoginGroup.master_confirmation)
async def confirm_master(message: types.Message, redirects: Redirects, **data) -> None:
    state: FSMContext = data['state']
    db: Database = data['db']

    user_data = await state.get_data()

    master = message.text

    async with db.session.begin():
        result = await db.user.confirm_master(message.from_user.id, master)

    if result:
        await Interactive.finish(
            message, state, user_data=user_data, state_clear=False,
            text='Операция подтверждена мастер-паролем ✅'
        )

        if user_data['save_master']:
            await state.update_data(master=master)

        await state.set_state(user_data['last_state'])
        await redirects.redirect(user_data['redirect'], message=message, **data)
    else:
        await Interactive.switch(
            message, state,
            user_data=user_data,
            text='Неверный мастер-пароль. Введи мастер-пароль ⬇️'
        )
