from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

MAIN_MENU_KB = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Мои пароли 📁'),
            KeyboardButton(text='Мой профиль 👨'),
        ],
        [
            KeyboardButton(text='Добавить ⏬'),
            KeyboardButton(text='Сгенерировать 🔑')
        ]
    ],
    resize_keyboard=True,
)
