from aiogram.fsm.state import StatesGroup, State


class RegisterGroup(StatesGroup):
    in_lobby = State()
    typing_password = State()
    typing_master = State()


class LoginGroup(StatesGroup):
    in_lobby = State()
    typing_password = State()
