from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.fsm import MainGroup

router = Router()


@router.callback_query(F.data == 'search_record', MainGroup.view_all_records)
async def type_query(call: types.CallbackQuery, state: FSMContext) -> None:
    # TODO: Реализовать поиск по записям.
    await call.message.answer('Введите запрос ⬇️ Например, "Google", "Google.com"')
    await state.set_state(MainGroup.searching_record)
    await call.answer()
