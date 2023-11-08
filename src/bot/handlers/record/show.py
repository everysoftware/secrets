from contextlib import suppress
from datetime import timedelta

from aiogram import Router, F, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from arq import ArqRedis

from src.bot.encryption import Encryption
from src.bot.fsm import MainGroup
from src.bot.fsm import RecordGroup
from src.bot.handlers.activities import ShowRecordControlActivity, ShowAllRecordsActivity
from src.bot.handlers.record.show_all import show_all_records_callback
from src.bot.handlers.user.confirm import send_confirmation_request
from src.bot.keyboards.record import RECORD_KB
from src.bot.schemes.handle import DecryptedRecordHandle
from src.bot.schemes.models import DecryptedRecord
from src.bot.utils.forwarding import redirects
from src.db import Database
from src.db.models import Record

router = Router(name='show_record')


@router.callback_query(F.data.startswith('show_record'), MainGroup.viewing_all_records)
@router.callback_query(F.data.startswith('show_record'), RecordGroup.viewing_record)
async def show_record_request(call: types.CallbackQuery, state: FSMContext) -> None:
    args = call.data.split('_')

    try:
        record_id = int(args[2])
    except (IndexError, ValueError):
        pass
    else:
        await state.update_data(record_id=record_id)
        await send_confirmation_request(call.message, state, show_record, save_master=True)
    finally:
        await call.answer()


@redirects.register_redirect
async def show_record(message: types.Message, state: FSMContext, db: Database, arq_redis: ArqRedis) -> None:
    user_data = await state.get_data()
    await ShowAllRecordsActivity.finish(
        message, state,
        user_data=user_data,
        state_clear=False  # Нужен record_id
    )

    async with db.session.begin():
        record: Record = await db.record.get(user_data['record_id'])
        decrypted = DecryptedRecord(
            record.title,
            Encryption.decrypt(record.username, user_data['master'], record.salt),
            Encryption.decrypt(record.password_, user_data['master'], record.salt),
            record.url,
            record.comment.text if record.comment else None
        )

    record_msg = await message.answer(DecryptedRecordHandle(decrypted).html())

    # Сообщение с данными пользователя отправляется отдельно от активности контрольной панели,
    # поэтому запоминаем вручную ID сообщения для последующих действий.
    await state.update_data(record_message_id=record_msg.message_id)

    await arq_redis.enqueue_job(
        'delete_message',
        _defer_by=timedelta(minutes=2),
        chat_id=message.from_user.id,
        message_id=record_msg.message_id
    )

    await show_record_cp(message, state, arq_redis)


async def show_record_cp(message: types.Message, state: FSMContext, arq_redis: ArqRedis) -> None:
    cp_msg = await ShowRecordControlActivity.start(
        message, state,
        RecordGroup.viewing_record,
        text='Ты в меню управления записью. Выбери действие 🔽',
        reply_markup=RECORD_KB
    )

    await arq_redis.enqueue_job(
        'delete_message',
        _defer_by=timedelta(minutes=2),
        chat_id=message.from_user.id,
        message_id=cp_msg.message_id
    )


@router.callback_query(F.data == 'back', RecordGroup.viewing_record)
async def back(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()

    # Подавляем исключение на случай, если сообщение уже было удалено планировщиком.
    with suppress(TelegramBadRequest):
        await call.message.chat.delete_message(user_data['record_message_id'])

    await ShowRecordControlActivity.finish_callback(
        call, state
    )

    await show_all_records_callback(call)
