from contextlib import suppress

from aiogram import Router, F, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup
from src.bot.fsm import RecordGroup
from src.bot.handlers.activities import ShowAllRecordsActivity
from src.bot.handlers.main import show_main_menu
from src.bot.keyboards.record import get_storage_kb
from src.db import Database

router = Router(name='show_all_records')


@router.message(MainGroup.viewing_main_menu, F.text == 'Мои пароли 📁')
@router.message(MainGroup.viewing_all_records, F.text == 'Мои пароли 📁')
@router.message(RecordGroup.viewing_record, F.text == 'Мои пароли 📁')
async def show_all_records(message: types.Message, state: FSMContext, db: Database) -> None:
    kb, new_offset = await get_storage_kb(message.from_user, db)

    await ShowAllRecordsActivity.start(
        message, state,
        new_state=MainGroup.viewing_all_records,
        text='<b>Ваши пароли</b>',
        reply_markup=kb
    )

    await state.update_data(offset=new_offset)


async def show_all_records_callback(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    kb, new_offset = await get_storage_kb(call.from_user, db)

    await ShowAllRecordsActivity.start_callback(
        call, state,
        new_state=MainGroup.viewing_all_records,
        text='<b>Ваши пароли</b>',
        reply_markup=kb
    )

    await state.update_data(offset=new_offset)


@router.callback_query(MainGroup.viewing_all_records, F.data == 'up')
async def up(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()
    kb, new_offset = await get_storage_kb(call.from_user, db, user_data['offset'], -10)

    with suppress(TelegramBadRequest):
        await call.message.edit_reply_markup(
            reply_markup=kb
        )

    await state.update_data(offset=new_offset)

    await call.answer()


@router.callback_query(MainGroup.viewing_all_records, F.data == 'down')
async def down(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()
    kb, new_offset = await get_storage_kb(call.from_user, db, user_data['offset'])

    with suppress(TelegramBadRequest):
        await call.message.edit_reply_markup(
            reply_markup=kb
        )

    await state.update_data(offset=new_offset)

    await call.answer()


@router.callback_query(MainGroup.viewing_all_records, F.data == 'back')
async def back(call: types.CallbackQuery, state: FSMContext) -> None:
    await ShowAllRecordsActivity.finish_callback(call, state)

    await show_main_menu(call.message, state)
