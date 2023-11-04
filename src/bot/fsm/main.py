from aiogram.fsm.state import StatesGroup, State


class MainGroup(StatesGroup):
    viewing_main_menu = State()
    viewing_storage = State()
    viewing_record = State()
    viewing_profile = State()


class ProfileActionsGroup(StatesGroup):
    updating_password = State()
    updating_master = State()
    deleting_account = State()


class ProfilePasswordEditingGroup(StatesGroup):
    typing_old_password = State()
    typing_new_password = State()


class RecordCreationGroup(StatesGroup):
    setting_title = State()
    setting_username = State()
    setting_password = State()


class RecordActionsGroup(StatesGroup):
    deleting_record = State()
    editing_record = State()


class RecordEditingGroup(StatesGroup):
    updating_title = State()
    updating_username = State()
    updating_password = State()
    updating_url = State()
    updating_comment = State()
