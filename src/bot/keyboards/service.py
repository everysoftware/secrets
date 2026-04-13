from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

CANCEL_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отмена ❌", callback_data="back"),
        ]
    ]
)

YESNO_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да ✅", callback_data="yes"),
            InlineKeyboardButton(text="Нет ❌", callback_data="no"),
        ]
    ]
)
