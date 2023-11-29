from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup, ProfileGroup
from src.bot.handlers.user.get import show_user
from src.bot.handlers.user.verify_id import id_verification_request
from src.bot.keyboards.service import YESNO_KB
from src.bot.utils.callback_manager import manager
from src.db import Database

router = Router()


@router.callback_query(F.data == 'delete_account', MainGroup.view_user)
async def delete_user_request(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer('Получен запрос на удаление аккаунта ❌')
    await id_verification_request(call.message, state, delete_account_yesno)
    await call.answer()


@manager.callback
async def delete_account_yesno(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        'Вы действительно хотите удалить аккаунт? Все сохранённые пароли будут безвозвратно потеряны!',
        reply_markup=YESNO_KB
    )
    await state.set_state(ProfileGroup.deleting_account)


@router.callback_query(F.data == 'yes', ProfileGroup.deleting_account)
async def delete_account_yes(
        call: types.CallbackQuery,
        state: FSMContext,
        db: Database
) -> None:
    async with db.session.begin():
        user = await db.user.get(call.from_user.id)
        await db.user.delete(user)

    await state.clear()
    await call.message.answer(
        'Аккаунт успешно удален ✅\n\n'
        'Если Вы хотите вернуться, пишите /start. Мы всегда будем рады Вас видеть! 🤗',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await call.answer()


@router.callback_query(F.data == 'no', ProfileGroup.deleting_account)
async def delete_account_no(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    await call.message.answer('Удаление аккаунта отменено ❌')
    await show_user(call, state, db)
    await call.answer()
