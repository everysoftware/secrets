from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

PROFILE_KB = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Сменить пароль 🔑'),
            KeyboardButton(text='Сменить мастер-пароль 🗝'),
        ],
        [
            KeyboardButton(text='Удалить аккаунт ❌'),
            KeyboardButton(text='Назад ◀️')
        ],
    ],
    resize_keyboard=True,
)
