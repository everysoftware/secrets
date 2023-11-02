from typing import Callable

from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext

from src.bot.encryption import verify_data
from src.bot.structures.fsm import LoginGroup
from src.db import Database
from .additional import update_last_message, edit_last_message
from .forwarding import Redirects
from ..filters import RegisterFilter
from ..middlewares import DatabaseMd

router = Router(name='confirmation')

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

router.message.filter(RegisterFilter())


async def confirm_master(
        msg: types.Message,
        state: FSMContext,
        redirect: Callable,
        save_master: bool = False
) -> None:
    await state.update_data(last_state=await state.get_state())
    await state.update_data(redirect=redirect.__name__)
    await state.update_data(save_master=save_master)

    sent_msg = await msg.answer('Для подтверждения операции введите мастер-пароль ⬇️')
    await update_last_message(state, sent_msg)
    await state.set_state(LoginGroup.master_confirmation)


@router.message(LoginGroup.master_confirmation)
async def confirm_master_helper(msg: types.Message, redirects: Redirects, **data) -> None:
    state: FSMContext = data['state']
    db: Database = data['db']
    bot: Bot = data['bot']

    user_data = await state.get_data()

    master = msg.text
    await msg.delete()

    async with db.session.begin():
        user = await db.user.get(msg.from_user.id)
        master_from_db = user.auth_data.master_password
        salt = user.auth_data.salt

    if verify_data(master, master_from_db, salt):
        await edit_last_message(bot, state, user_data, 'Операция подтверждена мастер-паролем ✅')
        if user_data['save_master']:
            await state.update_data(master=master)
        await state.set_state(user_data['last_state'])

        await redirects.redirect(user_data['redirect'], msg=msg, **data)
    else:
        await edit_last_message(bot, state, user_data, 'Неверный мастер-пароль. Введи мастер-пароль ⬇️')
