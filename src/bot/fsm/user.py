from aiogram.fsm.state import StatesGroup, State


class ProfileGroup(StatesGroup):
    updating_password = State()
    updating_master = State()
    deleting_account = State()


class ProfilePasswordEditingGroup(StatesGroup):
    typing_old_password = State()
    typing_new_password = State()


class ProfileMasterEditingGroup(StatesGroup):
    typing_old_password = State()
    typing_new_password = State()
