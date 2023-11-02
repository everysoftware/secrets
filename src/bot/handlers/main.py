from datetime import timedelta

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from arq import ArqRedis

from src.bot.encryption import generate_password
from src.bot.filters import RegisterFilter
from src.bot.middlewares import DatabaseMd
from src.bot.structures.fsm import MainGroup
from src.bot.structures.keyboards import MAIN_MENU_KB, get_storage_kb
from src.db import Database
from .additional import update_last_message

router = Router(name='main')

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

router.message.filter(RegisterFilter())
router.callback_query.filter(RegisterFilter())


async def show_main_menu(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(
        'Ты в главном меню. Используй кнопки для навигации 🔽',
        reply_markup=MAIN_MENU_KB
    )
    await state.set_state(MainGroup.viewing_main_menu)


@router.message(MainGroup.viewing_main_menu, F.text == 'Хранилище 📁')
@router.message(MainGroup.viewing_storage, F.text == 'Хранилище 📁')
@router.message(MainGroup.viewing_record, F.text == 'Хранилище 📁')
async def show_storage(msg: types.Message, state: FSMContext, db: Database) -> None:
    sent_msg = await msg.answer(
        '<b>Твои записи</b>',
        reply_markup=await get_storage_kb(msg, db),
    )
    await update_last_message(state, sent_msg)
    await state.set_state(MainGroup.viewing_storage)


@router.message(MainGroup.viewing_main_menu, F.text == 'Сгенерировать 🔑')
@router.message(MainGroup.viewing_storage, F.text == 'Сгенерировать 🔑')
@router.message(MainGroup.viewing_record, F.text == 'Сгенерировать 🔑')
async def gen_password(msg: types.Message, arq_redis: ArqRedis) -> None:
    password = generate_password()
    sent_msg = await msg.answer(
        f'🔑 Твой сгенерированный пароль:\n\n<code>{password}</code>'
    )
    await arq_redis.enqueue_job(
        'delete_message',
        _defer_by=timedelta(minutes=1),
        chat_id=msg.from_user.id,
        message_id=sent_msg.message_id,
    )


@router.message(MainGroup.viewing_main_menu, F.text == 'Мой профиль 👨')
@router.message(MainGroup.viewing_storage, F.text == 'Мой профиль 👨')
@router.message(MainGroup.viewing_record, F.text == 'Мой профиль 👨')
async def show_profile(msg: types.Message) -> None:
    await msg.answer('Меню профиля находится в разработке')
