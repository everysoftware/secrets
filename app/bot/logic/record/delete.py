from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from app.bot import RecordGroup
from app.bot.keyboards.service import YESNO_KB
from app.bot.logic.record.get import back_to_all_records
from app.core import Database

router = Router()


@router.callback_query(F.data == "delete_record", RecordGroup.view_record)
async def delete_record_question(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(
        "Вы действительно хотите удалить запись? Все данные, содержащиеся в ней, будут безвозвратно потеряны.",
        reply_markup=YESNO_KB,
    )
    await state.set_state(RecordGroup.delete_record)
    await call.answer()


@router.callback_query(F.data == "yes", RecordGroup.delete_record)
async def delete_record_yes(
        call: types.CallbackQuery, state: FSMContext, db: Database
) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        record = await db.record.get(user_data["record_id"])
        await db.record.delete(record)

    await call.message.answer("Запись успешно удалена ✅")
    await back_to_all_records(call, state, db)
    await call.answer()


@router.callback_query(F.data == "no", RecordGroup.delete_record)
async def delete_record_no(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(RecordGroup.view_record)
    await call.message.answer("Удаление записи отменено ❌")
    await call.answer()
