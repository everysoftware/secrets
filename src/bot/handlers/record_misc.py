from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.bot.filters import RegisterFilter
from src.bot.middlewares import DatabaseMd
from src.bot.structures.fsm import MainGroup

router = Router(name='record_misc')

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

router.message.filter(RegisterFilter())
router.callback_query.filter(RegisterFilter())


@router.callback_query(F.data == 'delete_msg_record', MainGroup.viewing_record)
async def delete_record_msg(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()

    await callback.message.chat.delete_message(user_data['record_msg_id'])
    await callback.message.delete()

    await state.set_state(MainGroup.viewing_storage)

    await callback.answer()
