from aiogram.fsm.state import StatesGroup, State


class MainGroup(StatesGroup):
    view_main_menu = State()
    view_all_records = State()
    view_user = State()
