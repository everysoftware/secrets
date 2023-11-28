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
    typing_title = State()
    typing_username = State()
    typing_password = State()
    typing_url = State()
    typing_comment = State()
