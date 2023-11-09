from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.handlers.activities import SearchRecordActivity
from src.bot.fsm import MainGroup

router = Router(name='search_record')


@router.callback_query(F.data == 'search_record', MainGroup.viewing_all_records)
async def type_url(call: types.CallbackQuery, state: FSMContext) -> None:
    # TODO: Реализовать поиск по записям.
    await SearchRecordActivity.start_callback(
        call, state,
        new_state=MainGroup.searching_record,
        text='Введите URL сайта'
    )
