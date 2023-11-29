from aiogram.fsm.state import StatesGroup, State


class VerificationGroup(StatesGroup):
    typing_master = State()
