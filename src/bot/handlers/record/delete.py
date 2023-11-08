from contextlib import suppress

from aiogram import Router, F, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from arq import ArqRedis

from src.bot.fsm import RecordGroup
from src.bot.handlers.activities import DeleteRecordActivity
from src.bot.handlers.record.show import show_record_cp, back
from src.bot.keyboards.service import YESNO_KB
from src.db import Database
from src.db.models import Record

router = Router(name='delete_record')


@router.callback_query(F.data == 'delete_record', RecordGroup.viewing_record)
async def delete_record(call: types.CallbackQuery, state: FSMContext) -> None:
    with suppress(TelegramBadRequest):
        await call.message.delete()

    await DeleteRecordActivity.start_callback(
        call, state,
        new_state=RecordGroup.deleting_record,
        text='Внимание! Удалив запись, ты безвозвратно потеряешь все данные, содержащиеся в ней. '
             'Ты действительно хочешь удалить запись?',
        reply_markup=YESNO_KB
    )


@router.callback_query(F.data == 'yes', RecordGroup.deleting_record)
async def delete_record_yes(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        await db.record.delete(Record.id == user_data['record_id'])

    await DeleteRecordActivity.finish_callback(
        call, state,
        text='Запись успешно удалена ✅',
        state_clear=False
    )
    await back(call, state, db)


@router.callback_query(F.data == 'no', RecordGroup.deleting_record)
async def delete_record_no(call: types.CallbackQuery, state: FSMContext, arq_redis: ArqRedis) -> None:
    await DeleteRecordActivity.finish_callback(
        call, state,
        text='Удаление записи отменено ❌',
        state_clear=False
    )
    await show_record_cp(call.message, state, arq_redis)
