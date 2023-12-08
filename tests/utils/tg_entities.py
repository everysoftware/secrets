import datetime
import random

from aiogram.types import User, Chat, Message, Update, CallbackQuery


def get_user(first_name='Ivan', **kwargs) -> User:
    return User(
        id=random.randint(1, 100),
        first_name=first_name,
        is_bot=False,
        **kwargs
    )


def get_chat(first_name=get_user().first_name, **kwargs) -> Chat:
    return Chat(
        id=random.randint(1, 100),
        type='private',
        first_name=first_name,
        **kwargs
    )


def get_message(
        date=datetime.datetime.now(),
        chat=get_chat(),
        from_user=get_user(),
        text='Hello world',
        **kwargs
) -> Message:
    return Message(
        message_id=random.randint(1, 100),
        date=date,
        chat=chat,
        from_user=from_user,
        text=text,
        **kwargs
    )


def get_update(
        message: Message | None = None,
        call: CallbackQuery | None = None,
        **kwargs
) -> Update:
    return Update(
        update_id=random.randint(1, 100),
        message=message,
        callback_query=call,
        **kwargs
    )
