from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup, ProfileGroup
from src.bot.handlers.activities import DeleteAccountActivity
from src.bot.handlers.main import show_profile
from src.bot.handlers.user.confirm import id_verification_request
from src.bot.keyboards.service import YESNO_KB
from src.bot.utils.callback_manager import manager
from src.db import Database

router = Router()


@router.message(MainGroup.viewing_profile, F.text == 'Удалить аккаунт ❌')
async def request(message: types.Message, state: FSMContext) -> None:
    await id_verification_request(message, state, delete_account_yesno)


@manager.callback
async def delete_account_yesno(message: types.Message, state: FSMContext) -> None:
    await DeleteAccountActivity.start(
        message, state,
        new_state=ProfileGroup.deleting_account,
        text='Внимание! Удалив аккаунт, Вы безвозвратно потеряете все сохранённые пароли! '
             'Вы действительно хотите удалить аккаунт?',
        reply_markup=YESNO_KB
    )


@router.callback_query(ProfileGroup.deleting_account, F.data == 'yes')
async def delete_account_yes(
        call: types.CallbackQuery,
        state: FSMContext,
        db: Database
) -> None:
    async with db.session.begin():
        user = await db.user.get(call.from_user.id)
        await db.user.delete(user)

    await DeleteAccountActivity.finish_callback(
        call, state
    )
    await state.clear()
    await call.message.answer(
        'Аккаунт успешно удален ✅\n\n'
        'Если Вы хотите вернуться, пишите /start. Мы всегда будем рады Вас видеть! 🤗',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await call.answer()


@router.callback_query(ProfileGroup.deleting_account, F.data == 'no')
async def delete_account_no(call: types.CallbackQuery, state: FSMContext) -> None:
    await DeleteAccountActivity.finish_callback(
        call, state,
        new_state=MainGroup.viewing_profile,
        text='Удаление аккаунта отменено ❌'
    )
    await show_profile(call.message, state)
    await call.answer()
