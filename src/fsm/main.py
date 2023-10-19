from aiogram.fsm.state import StatesGroup, State


class MainGroup(StatesGroup):
    main_menu = State()
    address_step = State()
    title_step = State()
    username_step = State()
    password_step = State()
    records_step = State()
