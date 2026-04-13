from aiogram.fsm.state import State, StatesGroup


class MainGroup(StatesGroup):
    view_main_menu = State()
    view_all_records = State()
    view_user = State()
