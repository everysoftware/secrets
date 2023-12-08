from aiogram.fsm.state import State, StatesGroup


class RegisterGroup(StatesGroup):
    in_lobby = State()
    type_password = State()
    type_master = State()


class LoginGroup(StatesGroup):
    type_password = State()
