from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from src.bot.fsm import MainGroup
from src.bot.fsm import RecordGroup
from src.bot.handlers.main import show_main_menu
from src.bot.keyboards.record import get_storage_kb
from src.db import Database
from src.db.models import Record
from src.db.models import User

router = Router()


async def _show_all_records(update: types.Message | types.CallbackQuery, state: FSMContext, db: Database) -> None:
    async with db.session.begin():
        stmt = select(func.count(Record.id)).where(Record.user_id == update.from_user.id)
        res = await db.session.execute(stmt)
        count = res.scalar_one()
        user = await db.user.get(update.from_user.id, options=[selectinload(User.records)])

    kb = await get_storage_kb(user.records)
    message = update if isinstance(update, types.Message) else update.message
    await message.answer(
        '<b>Мои пароли</b>\n\n'
        f'🔢 Количество: {count}\n'
        f'📝 Порядок сортировки: по алфавиту',
        reply_markup=kb)
    await state.set_state(MainGroup.viewing_all_records)


@router.message(MainGroup.viewing_main_menu, F.text == 'Мои пароли 📁')
@router.message(MainGroup.viewing_all_records, F.text == 'Мои пароли 📁')
@router.message(RecordGroup.viewing_record, F.text == 'Мои пароли 📁')
async def show_all_records(message: types.Message, state: FSMContext, db: Database) -> None:
    await _show_all_records(message, state, db)


#
#
# @router.callback_query(MainGroup.viewing_all_records, F.data == 'up')
# async def up(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
#     user_data = await state.get_data()
#     kb, new_offset = await get_storage_kb(call.from_user, db, user_data['offset'], -10)
#
#     with suppress(TelegramBadRequest):
#         await call.message.edit_reply_markup(
#             reply_markup=kb
#         )
#
#     await state.update_data(offset=new_offset)
#
#     await call.answer()
#
#
# @router.callback_query(MainGroup.viewing_all_records, F.data == 'down')
# async def down(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
#     user_data = await state.get_data()
#     kb, new_offset = await get_storage_kb(call.from_user, db, user_data['offset'])
#
#     with suppress(TelegramBadRequest):
#         await call.message.edit_reply_markup(
#             reply_markup=kb
#         )
#
#     await state.update_data(offset=new_offset)
#
#     await call.answer()


@router.callback_query(MainGroup.viewing_all_records, F.data == 'back')
async def back(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await show_main_menu(call.message, state)
    await call.answer()
