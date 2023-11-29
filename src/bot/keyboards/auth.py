from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

REG_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Регистрация ⚡️')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
