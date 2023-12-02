from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from api.auth.schemes import User
from bot.fsm import MainGroup, RecordGroup
from bot.keyboards.user import PROFILE_KB
from bot.logic.main import show_main_menu
from services.db import Database

router = Router()


async def show_user(
    update: types.Message | types.CallbackQuery, state: FSMContext, db: Database
) -> None:
    async with db.session.begin():
        user = await db.user.get(update.from_user.id)

    message = update if isinstance(update, types.Message) else update.message
    await message.answer(User.model_validate(user).html(), reply_markup=PROFILE_KB)
    await state.set_state(MainGroup.view_user)


@router.message(MainGroup.view_main_menu, F.text == "Мой профиль 👨")
@router.message(MainGroup.view_all_records, F.text == "Мой профиль 👨")
@router.message(RecordGroup.view_record, F.text == "Мой профиль 👨")
@router.message(MainGroup.view_user, F.text == "Мой профиль 👨")
async def process_message(
    message: types.Message, state: FSMContext, db: Database
) -> None:
    await show_user(message, state, db)


@router.callback_query(F.data == "back", MainGroup.view_user)
async def back_to_menu(call: types.CallbackQuery, state: FSMContext) -> None:
    await show_main_menu(call.message, state)
    await call.answer()
