from typing import Callable

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import joinedload

from src.bot.fsm import VerificationGroup
from src.bot.keyboards.service import CANCEL_KB
from src.bot.utils.callback_manager import CallbackManager
from src.bot.utils.security import DataVerification
from src.db import Database
from src.db.models import User

router = Router()


async def id_verification_request(
        message: types.Message,
        state: FSMContext,
        redirect: Callable,
        save_master: bool = False
) -> None:
    await state.update_data(last_state=await state.get_state())
    await state.update_data(redirect=hash(redirect))
    await state.update_data(save_master=save_master)

    await message.answer('Для подтверждения вашей личности введите мастер-пароль ⬇️', reply_markup=CANCEL_KB)
    await state.set_state(VerificationGroup.typing_master)


@router.callback_query(VerificationGroup.typing_master, F.data == 'back')
async def back(call: types.CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    await state.set_state(user_data['last_state'])

    await call.message.answer('Операция отменена ❌')
    await call.answer()


@router.message(VerificationGroup.typing_master)
async def confirm_master(
        message: types.Message,
        manager: CallbackManager,
        state: FSMContext,
        db: Database,
        **data
) -> None:
    await message.delete()

    data |= {'message': message, 'db': db, 'state': state}
    master = message.text

    async with db.session.begin():
        user = await db.user.get(message.from_user.id, options=[joinedload(User.auth_data)])
        result = DataVerification.verify(master, user.auth_data.master_password, user.auth_data.salt)

    user_data = await state.get_data()
    if result:
        await message.answer('Мастер-пароль верный ✅')

        if user_data['save_master']:
            await state.update_data(master=master)

        await state.set_state(user_data['last_state'])
        await manager.invoke(user_data['redirect'], **data)
    else:
        await message.answer('Мастер-пароль неверный. Попробуйте ещё раз ⬇️', reply_markup=CANCEL_KB)
