from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup, RecordActionsGroup
from src.bot.keyboards import YESNO_KB
from src.bot.utils.messages import Interactive
from src.db import Database
from src.db.models import Record

router = Router(name='record_removal')


@router.callback_query(F.data == 'delete_record', MainGroup.viewing_record)
async def delete_record(call: types.CallbackQuery, state: FSMContext) -> None:
    await Interactive.start(
        call.message, state,
        new_state=RecordActionsGroup.deleting_record,
        text='Внимание! Удалив запись, ты безвозвратно потеряешь все данные, содержащиеся в ней. '
             'Ты действительно хочешь удалить запись?',
        reply_markup=YESNO_KB
    )

    await call.answer()


@router.callback_query(F.data == 'yes', RecordActionsGroup.deleting_record)
async def delete_record_yes(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        await db.record.delete(Record.id == user_data['record_id'])

    await Interactive.finish_callback(
        call.message, state,
        new_state=MainGroup.viewing_storage,
        text='Запись успешно удалена ✅',
        state_clear=False
    )

    await call.answer()


@router.callback_query(F.data == 'no', RecordActionsGroup.deleting_record)
async def delete_record_no(call: types.CallbackQuery, state: FSMContext) -> None:
    await Interactive.finish_callback(
        call.message, state,
        new_state=MainGroup.viewing_record,
        text='Удаление записи отменено ❌',
        state_clear=False
    )

    await call.answer()
