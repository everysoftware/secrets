from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

AUTH_KB = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="Авторизация ⚡️",
                web_app=WebAppInfo(
                    url="https://everysoftware.github.io/secrets/web/auth"
                ),
            )
        ]
    ],
    resize_keyboard=True,
)

REG_KB = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Регистрация ⚡️")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)
