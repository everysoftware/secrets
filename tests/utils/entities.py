import datetime
from typing import Optional

from aiogram.types import User, Chat, Message, Update, CallbackQuery


def get_user(
        id=123,
        is_bot=False,
        first_name='Test',
        last_name='User',
        username='test_user',
        language_code='ru-RU',
        is_premium=True,
        **kwargs
):
    return User(
        id=id,
        is_bot=is_bot,
        first_name=first_name,
        last_name=last_name,
        username=username,
        language_code=language_code,
        is_premium=is_premium,
        **kwargs
    )


def get_chat(
        id=321,
        type='private',
        username=get_user().username,
        first_name=get_user().first_name,
        last_name=get_user().last_name,
        **kwargs
):
    return Chat(
        id=id,
        type=type,
        username=username,
        first_name=first_name,
        last_name=last_name,
        **kwargs
    )


def get_message(
        message_id=111,
        date=datetime.datetime.now(),
        chat=get_chat(),
        from_user=get_user(),
        text='test message',
        **kwargs
):
    return Message(
        message_id=message_id,
        date=date,
        chat=chat,
        from_user=from_user,
        text=text,
        **kwargs
    )


def get_update(
        message: Optional[Message] = None,
        call: Optional[CallbackQuery] = None,
        **kwargs
):
    return Update(
        update_id=222,
        message=message,
        callback_query=call,
        **kwargs
    )
