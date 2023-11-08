from aiogram.fsm.state import StatesGroup, State


class RecordGroup(StatesGroup):
    viewing_record = State()
    deleting_record = State()
    editing_record = State()


class AddRecordGroup(StatesGroup):
    typing_title = State()
    typing_username = State()
    typing_password = State()


class UpdateRecordGroup(StatesGroup):
    updating_title = State()
    updating_username = State()
    updating_password = State()
    updating_url = State()
    updating_comment = State()
