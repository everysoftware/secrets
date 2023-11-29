from aiogram.fsm.state import StatesGroup, State


class RegisterGroup(StatesGroup):
    in_lobby = State()
    type_password = State()
    type_master = State()


class LoginGroup(StatesGroup):
    in_lobby = State()
    type_password = State()
