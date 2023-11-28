from datetime import timedelta
from html import escape

from aiogram import Router, types, F
from aiogram.filters import Command
from arq import ArqRedis

from src.bot.fsm import MainGroup, RecordGroup
from src.bot.security import generate_password

router = Router()


@router.message(MainGroup.viewing_main_menu, F.text == 'Предложить 🔑')
@router.message(MainGroup.viewing_all_records, F.text == 'Предложить 🔑')
@router.message(RecordGroup.viewing_record, F.text == 'Предложить 🔑')
@router.message(Command('suggest'))
async def suggest_password(message: types.Message, arq_redis: ArqRedis) -> types.Message:
    password = generate_password()
    sent_msg = await message.answer(
        f'Ваш случайный пароль:\n\n<code>{escape(password)}</code>'
    )
    await arq_redis.enqueue_job(
        'delete_message',
        _defer_by=timedelta(minutes=1),
        chat_id=message.from_user.id,
        message_id=sent_msg.message_id,
    )
    return sent_msg
