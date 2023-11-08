from aiogram import Router, F, types
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
    await ShowAllRecordsActivity.start(
        message, state,
        new_state=MainGroup.viewing_all_records,
        text='<b>Твои пароли</b>',
        reply_markup=await get_storage_kb(message.from_user, db)
    )


async def show_all_records_callback(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    await ShowAllRecordsActivity.start_callback(
        call, state,
        new_state=MainGroup.viewing_all_records,
        text='<b>Твои пароли</b>',
        reply_markup=await get_storage_kb(call.from_user, db)
    )


@router.callback_query(MainGroup.viewing_all_records, F.data == 'back')
async def back(call: types.CallbackQuery, state: FSMContext) -> None:
    await ShowAllRecordsActivity.finish_callback(call, state)

    await show_main_menu(call.message, state)
