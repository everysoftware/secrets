from aiogram.fsm.state import StatesGroup, State


class RecordGroup(StatesGroup):
    view_record = State()
    delete_record = State()
    edit_record = State()
    find_record = State()


class AddRecordGroup(StatesGroup):
    type_title = State()
    type_username = State()
    type_password = State()


class EditRecordGroup(StatesGroup):
    type_title = State()
    type_username = State()
    type_password = State()
    type_url = State()
    type_comment = State()
