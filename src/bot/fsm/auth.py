from aiogram.fsm.state import StatesGroup, State


class RegisterGroup(StatesGroup):
    waiting_for_click = State()
    entering_password = State()
    entering_master = State()


class LoginGroup(StatesGroup):
    waiting_for_click = State()
    typing_password = State()
    master_confirmation = State()
