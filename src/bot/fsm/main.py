from aiogram.fsm.state import StatesGroup, State


class MainGroup(StatesGroup):
    viewing_main_menu = State()
    viewing_all_records = State()
    searching_record = State()
    viewing_profile = State()
