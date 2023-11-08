from aiogram.fsm.state import StatesGroup, State


class ConfirmationGroup(StatesGroup):
    typing_master = State()
