from datetime import timedelta

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from arq import ArqRedis
from sqlalchemy.orm import joinedload

from src.bot.factories import ShowRecordData
from src.bot.fsm import RecordGroup, MainGroup
from src.bot.handlers.record.get_all import _show_all_records
from src.bot.handlers.user.verify_id import id_verification_request
from src.bot.keyboards.record import RECORD_KB
from src.bot.schemes.handle import DecryptedRecordHandle
from src.bot.schemes.models import DecryptedRecord
from src.bot.security import Encryption
from src.bot.utils.callback_manager import manager
from src.db import Database
from src.db.models import Record

router = Router()


@router.callback_query(ShowRecordData.filter(), MainGroup.viewing_all_records)
async def show_record_request(call: types.CallbackQuery, callback_data: ShowRecordData, state: FSMContext) -> None:
    await call.message.answer(f'Получен запрос на просмотр пароля {callback_data.record_name} 📝')
    await state.update_data(record_id=callback_data.record_id)
    await id_verification_request(call.message, state, show_record, save_master=True)
    await call.answer()


@manager.callback
async def show_record(message: types.Message, state: FSMContext, db: Database, arq_redis: ArqRedis) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        record = await db.record.get(user_data['record_id'], options=[joinedload(Record.comment)])
        decrypted = DecryptedRecord(
            id=record.id,
            title=record.title,
            username=Encryption.decrypt(record.username, user_data['master'], record.salt),
            password=Encryption.decrypt(record.password_, user_data['master'], record.salt),
            url=record.url,
            comment=record.comment.text if record.comment else None,
            created_at=record.created_at,
            updated_at=record.updated_at
        )

    await message.answer(
        'Используйте кнопки ниже для управления паролем.\n'
        'Сообщение будет удалено через 2 минуты ⏱️'
    )
    record_msg = await message.answer(DecryptedRecordHandle(decrypted).html(), reply_markup=RECORD_KB)
    await state.set_state(RecordGroup.viewing_record)
    await arq_redis.enqueue_job(
        'delete_message',
        _defer_by=timedelta(minutes=2),
        chat_id=message.from_user.id,
        message_id=record_msg.message_id
    )


@router.callback_query(F.data == 'back', RecordGroup.viewing_record)
async def back(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    await state.clear()
    await _show_all_records(call, state, db)
    await call.answer()
