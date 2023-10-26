from aiogram.fsm.state import StatesGroup, State


class MainGroup(StatesGroup):
    viewing_main_menu = State()
    setting_url = State()
    setting_title = State()
    setting_username = State()
    setting_password = State()
    viewing_storage = State()
    viewing_record = State()
    deleting_record = State()
    editing_record = State()
