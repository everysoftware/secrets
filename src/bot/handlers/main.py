from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from arq import ArqRedis

from src.bot.filters import RegisterFilter
from src.bot.fsm import MainGroup
from src.bot.fsm import RecordGroup
from src.bot.handlers.start import suggest
from src.bot.keyboards.main import MAIN_MENU_KB
from src.bot.keyboards.user import PROFILE_KB
from src.bot.middlewares import DatabaseMd

router = Router(name='main')

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

router.message.filter(RegisterFilter())
router.callback_query.filter(RegisterFilter())


@router.message(MainGroup.viewing_profile, F.text == 'Назад ◀️')
async def show_main_menu(message: types.Message, state: FSMContext) -> None:
    await state.clear()

    await message.answer(
        'Вы в главном меню. Выберите действие 🔽',
        reply_markup=MAIN_MENU_KB
    )

    await state.set_state(MainGroup.viewing_main_menu)


@router.message(MainGroup.viewing_main_menu, F.text == 'Предложить 🔑')
@router.message(MainGroup.viewing_all_records, F.text == 'Предложить 🔑')
@router.message(RecordGroup.viewing_record, F.text == 'Предложить 🔑')
async def suggest_password(message: types.Message, arq_redis: ArqRedis) -> None:
    await suggest(message, arq_redis)


@router.message(MainGroup.viewing_main_menu, F.text == 'Мой профиль 👨')
@router.message(MainGroup.viewing_all_records, F.text == 'Мой профиль 👨')
@router.message(RecordGroup.viewing_record, F.text == 'Мой профиль 👨')
async def show_profile(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        text='Вы в меню профиля. Выберите действие 🔽',
        reply_markup=PROFILE_KB
    )
    await state.set_state(MainGroup.viewing_profile)
