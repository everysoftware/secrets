from math import ceil
from typing import Sequence

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy import func, select

from app.bot import MainGroup, RecordGroup
from app.bot.keyboards.record import get_storage_kb
from app.bot.logic.main import show_main_menu
from app.core import Database, Record

router = Router()

PER_PAGE = 10


async def paginate_records(
    db: Database, user_id: int, page: int = 1
) -> Sequence[Record]:
    """Функция пагинации для модели Record."""
    # Создайте запрос с помощью select
    stmt = select(Record).where(Record.user_id == user_id).order_by(Record.name)

    # Вычисляем смещение для запроса
    offset = (page - 1) * PER_PAGE

    # Добавляем limit и offset к запросу
    stmt = stmt.limit(PER_PAGE).offset(offset)

    # Выполняем запрос
    result = await db.session.execute(stmt)

    # Получаем записи для текущей страницы
    records = result.scalars().all()

    return records


async def show_all_records(
    update: types.Message | types.CallbackQuery, state: FSMContext, db: Database
) -> None:
    async with db.session.begin():
        stmt = select(func.count(Record.id)).where(
            Record.user_id == update.from_user.id
        )
        res = await db.session.execute(stmt)
        count = res.scalar_one()

    records = await paginate_records(db, update.from_user.id)
    await state.update_data(page=1)
    await state.update_data(page_count=ceil(count / PER_PAGE))

    message = update if isinstance(update, types.Message) else update.message
    await message.answer(
        "<b>Мои пароли</b>\n\n"
        f"🔢 Количество: {count}\n"
        f"📝 Порядок сортировки: по алфавиту",
        reply_markup=await get_storage_kb(records),
    )
    await state.set_state(MainGroup.view_all_records)


@router.message(MainGroup.view_main_menu, F.text == "Мои пароли 📁")
@router.message(MainGroup.view_all_records, F.text == "Мои пароли 📁")
@router.message(RecordGroup.view_record, F.text == "Мои пароли 📁")
@router.message(MainGroup.view_user, F.text == "Мои пароли 📁")
async def process_message(
    message: types.Message, state: FSMContext, db: Database
) -> None:
    await show_all_records(message, state, db)


@router.callback_query(MainGroup.view_all_records, F.data == "up")
async def up(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()
    page = user_data["page"]

    if page == 1:
        await call.answer()
        return

    page -= 1
    records = await paginate_records(db, call.from_user.id, page)
    await call.message.edit_reply_markup(reply_markup=await get_storage_kb(records))

    await state.update_data(page=page)
    await call.answer()


@router.callback_query(MainGroup.view_all_records, F.data == "down")
async def down(call: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()
    page = user_data["page"]

    if page >= user_data["page_count"]:
        await call.answer()
        return

    page += 1
    records = await paginate_records(db, call.from_user.id, page)
    await call.message.edit_reply_markup(reply_markup=await get_storage_kb(records))

    await state.update_data(page=page)
    await call.answer()


@router.callback_query(MainGroup.view_all_records, F.data == "back")
async def back(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await show_main_menu(call.message, state)
    await call.answer()
