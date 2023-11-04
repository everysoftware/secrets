from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from arq import ArqRedis

from src.bot.filters import RegisterFilter
from src.bot.fsm import MainGroup
from src.bot.handlers.start import generate
from src.bot.keyboards import MAIN_MENU_KB, get_storage_kb
from src.bot.keyboards.main import PROFILE_KB
from src.bot.middlewares import DatabaseMd
from src.db import Database

router = Router(name='main')

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

router.message.filter(RegisterFilter())
router.callback_query.filter(RegisterFilter())


@router.message(MainGroup.viewing_profile, F.text == 'Назад ◀️')
async def show_main_menu(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        'Ты в главном меню. Используй кнопки для навигации 🔽',
        reply_markup=MAIN_MENU_KB
    )
    await state.set_state(MainGroup.viewing_main_menu)


@router.message(MainGroup.viewing_main_menu, F.text == 'Хранилище 📁')
@router.message(MainGroup.viewing_storage, F.text == 'Хранилище 📁')
@router.message(MainGroup.viewing_record, F.text == 'Хранилище 📁')
async def show_storage(message: types.Message, state: FSMContext, db: Database) -> None:
    await message.answer(
        '<b>Твои записи</b>',
        reply_markup=await get_storage_kb(message, db),
    )
    await state.set_state(MainGroup.viewing_storage)


@router.message(MainGroup.viewing_main_menu, F.text == 'Сгенерировать 🔑')
@router.message(MainGroup.viewing_storage, F.text == 'Сгенерировать 🔑')
@router.message(MainGroup.viewing_record, F.text == 'Сгенерировать 🔑')
async def generate_password(message: types.Message, arq_redis: ArqRedis) -> None:
    await generate(message, arq_redis)


@router.message(MainGroup.viewing_main_menu, F.text == 'Мой профиль 👨')
@router.message(MainGroup.viewing_storage, F.text == 'Мой профиль 👨')
@router.message(MainGroup.viewing_record, F.text == 'Мой профиль 👨')
async def show_profile(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(
        'Ты в меню профиля. Используй кнопки для навигации 🔽',
        reply_markup=PROFILE_KB
    )
    await state.set_state(MainGroup.viewing_profile)
