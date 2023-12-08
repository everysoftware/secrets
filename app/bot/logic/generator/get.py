from datetime import timedelta
from html import escape

from aiogram import F, Router, types
from aiogram.filters import Command
from arq import ArqRedis
from utils import generate_password

from app.bot import MainGroup, RecordGroup

router = Router()


@router.message(MainGroup.view_main_menu, F.text == "Предложить 🔑")
@router.message(MainGroup.view_all_records, F.text == "Предложить 🔑")
@router.message(RecordGroup.view_record, F.text == "Предложить 🔑")
@router.message(MainGroup.view_user, F.text == "Предложить 🔑")
@router.message(Command("suggest"))
async def suggest_password(message: types.Message, rq: ArqRedis) -> types.Message:
    password = generate_password()
    sent_msg = await message.answer(
        f"Ваш случайный пароль:\n\n<code>{escape(password)}</code>"
    )
    await rq.enqueue_job(
        "delete_message",
        _defer_by=timedelta(minutes=1),
        chat_id=message.from_user.id,
        message_id=sent_msg.message_id,
    )
    return sent_msg
