from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

PROFILE_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Сменить пароль 🔑', callback_data='change_password'),
            InlineKeyboardButton(text='Сменить мастер-пароль 🗝', callback_data='change_master'),
        ],
        [
            InlineKeyboardButton(text='Удалить аккаунт ❌', callback_data='delete_account'),
            InlineKeyboardButton(text='Назад ◀️', callback_data='back')
        ],
    ],
)
