from aiogram.fsm.state import State, StatesGroup


class VerificationGroup(StatesGroup):
    typing_master = State()
