from typing import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.factories import ShowRecordData
from services.db.models import Record


async def get_storage_kb(records: Sequence[Record]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # TODO: Оптимизировать скроллинг паролей
    for record in records:
        builder.add(
            InlineKeyboardButton(
                text=record.title,
                callback_data=ShowRecordData(
                    record_id=record.id, record_name=record.title
                ).pack(),
            )
        )

    builder.adjust(1)
    builder.row(
        InlineKeyboardButton(text="🔼", callback_data="up"),
        InlineKeyboardButton(text="Назад ◀️", callback_data="back"),
        InlineKeyboardButton(text="🔽", callback_data="down"),
    )
    return builder.as_markup(resize_keyboard=True)


RECORD_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️", callback_data="edit_record"),
            InlineKeyboardButton(text="❌", callback_data="delete_record"),
            InlineKeyboardButton(text="◀️", callback_data="back"),
        ]
    ]
)

EDIT_RECORD_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Имя пароля 🌐", callback_data="edit_title"),
            InlineKeyboardButton(
                text="Имя пользователя 👨", callback_data="edit_username"
            ),
        ],
        [
            InlineKeyboardButton(text="Пароль 🔑", callback_data="edit_password"),
            InlineKeyboardButton(text="Веб-сайт 🔗", callback_data="edit_url"),
        ],
        [
            InlineKeyboardButton(text="Комментарий 💬", callback_data="edit_comment"),
            InlineKeyboardButton(text="Назад ◀️", callback_data="back"),
        ],
    ]
)
