from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from app.bot import MainGroup, RecordGroup

router = Router()


@router.callback_query(F.data == "search_record", MainGroup.view_all_records)
async def type_query(call: types.CallbackQuery, state: FSMContext) -> None:
    # TODO: Реализовать поиск по записям.
    await call.message.answer('Введите запрос ⬇️ Например, "Google", "Google.com"')
    await state.set_state(RecordGroup.find_record)
    await call.answer()
