from aiogram.fsm.state import StatesGroup, State


class RegisterGroup(StatesGroup):
    button_step = State()
    entering_password = State()
    entering_master = State()


class LoginGroup(StatesGroup):
    button_step = State()
    entering_password = State()
    master_confirmation = State()
