from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy import text

from src.bot.fsm import MainGroup, ProfileGroup
from src.bot.handlers.activities import DeleteAccountActivity
from src.bot.handlers.main import show_profile
from src.bot.handlers.start import start
from src.bot.handlers.user.confirm import send_confirmation_request
from src.bot.keyboards.service import YESNO_KB
from src.bot.utils.forwarding import redirects
from src.cache import Cache
from src.db import Database

router = Router(name='delete_user')


@router.message(MainGroup.viewing_profile, F.text == 'Удалить аккаунт ❌')
async def delete_account_confirmation(message: types.Message, state: FSMContext) -> None:
    await send_confirmation_request(message, state, delete_account_yesno)


@redirects.register_redirect
async def delete_account_yesno(message: types.Message, state: FSMContext) -> None:
    await DeleteAccountActivity.start(
        message, state,
        new_state=ProfileGroup.deleting_account,
        text='Внимание! Удалив аккаунт, ты безвозвратно потеряешь все сохранённые пароли! '
             'Ты действительно хочешь удалить аккаунт?',
        reply_markup=YESNO_KB
    )


@router.callback_query(ProfileGroup.deleting_account, F.data == 'yes')
async def delete_account_yes(
        call: types.CallbackQuery,
        state: FSMContext,
        db: Database,
        cache: Cache
) -> None:
    async with db.session.begin():
        await db.session.execute(
            text("DELETE FROM users WHERE user_id = :user_id"),
            {'user_id': call.from_user.id}
        )

    await cache.delete(f'user_exists:{call.from_user.id}')

    await DeleteAccountActivity.finish_callback(
        call, state,
        text='Аккаунт успешно удален ✅'
    )

    await start(call.message, state, cache)


@router.callback_query(ProfileGroup.deleting_account, F.data == 'no')
async def delete_account_no(call: types.CallbackQuery, state: FSMContext) -> None:
    await DeleteAccountActivity.finish_callback(
        call, state,
        new_state=MainGroup.viewing_profile,
        text='Удаление аккаунта отменено ❌'
    )

    await show_profile(call.message, state)
