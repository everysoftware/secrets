from typing import Callable

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.fsm import ConfirmationGroup
from src.bot.handlers.activities import ConfirmMasterActivity
from src.bot.keyboards.service import CANCEL_KB
from src.bot.utils.forwarding import Redirects
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

    await ConfirmMasterActivity.start(
        message, state, ConfirmationGroup.typing_master,
        text='Для подтверждения вашей личности введите мастер-пароль ⬇️',
        reply_markup=CANCEL_KB
    )


@router.callback_query(ConfirmationGroup.typing_master, F.data == 'back')
async def back(call: types.CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    await state.set_state(user_data['last_state'])

    await ConfirmMasterActivity.finish_callback(
        call, state,
        text='Операция отменена ❌'
    )


@router.message(ConfirmationGroup.typing_master)
async def confirm_master(message: types.Message, redirects: Redirects, **data) -> None:
    state: FSMContext = data['state']
    db: Database = data['db']

    user_data = await state.get_data()

    master = message.text

    async with db.session.begin():
        result = await db.user.confirm_master(message.from_user.id, master)

    if result:
        await ConfirmMasterActivity.finish(
            message, state,
            user_data=user_data
        )

        if user_data['save_master']:
            await state.update_data(master=master)

        await state.set_state(user_data['last_state'])
        await redirects.redirect(user_data['redirect'], message=message, **data)
    else:
        await ConfirmMasterActivity.switch(
            message, state,
            user_data=user_data,
            text='Неверный мастер-пароль. Введите мастер-пароль ⬇️',
            reply_markup=CANCEL_KB
        )
