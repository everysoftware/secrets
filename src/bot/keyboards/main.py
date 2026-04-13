from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

MAIN_MENU_KB = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Мои пароли 📁"),
            KeyboardButton(text="Мой профиль 👨"),
        ],
        [KeyboardButton(text="Добавить ⏬"), KeyboardButton(text="Предложить 🔑")],
    ],
    resize_keyboard=True,
)
