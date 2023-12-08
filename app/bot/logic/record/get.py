from datetime import timedelta

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from arq import ArqRedis
from sqlalchemy.orm import joinedload

from app.bot import MainGroup, RecordGroup, ShowRecordData, manager
from app.bot.keyboards.record import RECORD_KB
from app.bot.logic import show_all_records
from app.bot.logic.user import id_verification_request
from app.core import Database, Record

router = Router()


@router.callback_query(ShowRecordData.filter(), MainGroup.view_all_records)
async def show_record_request(
    call: types.CallbackQuery, callback_data: ShowRecordData, state: FSMContext
) -> None:
    await call.message.answer(
        f"Получен запрос на просмотр пароля {callback_data.record_name} 📝"
    )
    await state.update_data(record_id=callback_data.record_id)
    await id_verification_request(
        call.message, state, process_callback, save_master=True
    )
    await call.answer()


async def show_record(
    update: types.Message | types.CallbackQuery,
    state: FSMContext,
    db: Database,
    rq: ArqRedis,
) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        record = await db.record.get(
            user_data["record_id"], options=[joinedload(Record.comment)]
        )

    decrypted = db.record.decrypt(record, user_data["master"])
    message = update if isinstance(update, types.Message) else update.message
    record_msg = await message.answer(decrypted.html(), reply_markup=RECORD_KB)
    await state.set_state(RecordGroup.view_record)

    await rq.enqueue_job(
        "delete_message",
        _defer_by=timedelta(minutes=2),
        chat_id=update.from_user.id,
        message_id=record_msg.message_id,
    )


@manager.callback
async def process_callback(
    message: types.Message, state: FSMContext, db: Database, rq: ArqRedis
) -> None:
    await show_record(message, state, db, rq)


@router.callback_query(F.data == "back", RecordGroup.view_record)
async def back_to_all_records(
    call: types.CallbackQuery, state: FSMContext, db: Database
) -> None:
    await state.clear()
    await show_all_records(call, state, db)
    await call.answer()
