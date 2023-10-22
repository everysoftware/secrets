from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_reg_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Регистрация ✔️')]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_login_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Авторизация 😇')]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
