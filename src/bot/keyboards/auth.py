from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

REG_KB = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Регистрация ⚡️")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)
