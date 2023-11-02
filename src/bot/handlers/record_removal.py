from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.filters import RegisterFilter
from src.bot.handlers.confirmation import confirm_master
from src.bot.handlers.forwarding import redirects
from src.bot.middlewares import DatabaseMd
from src.bot.structures.fsm import MainGroup, RecordActionsGroup
from src.bot.structures.keyboards import YESNO_KB
from src.db import Database
from src.db.models import Record

router = Router(name='record_removal')

router.message.middleware(DatabaseMd())
router.callback_query.middleware(DatabaseMd())

router.message.filter(RegisterFilter())
router.callback_query.filter(RegisterFilter())


@router.callback_query(F.data == 'delete_record', MainGroup.viewing_record)
async def delete_record_confirmation(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(RecordActionsGroup.deleting_record)
    await confirm_master(callback.message, state, delete_record_yesno)
    await callback.answer()


@redirects.register_redirect
async def delete_record_yesno(msg: types.Message) -> None:
    await msg.answer(
        'После удаления записи её нельзя будет восстановить. Ты действительно хочешь удалить запись?',
        reply_markup=YESNO_KB
    )


@router.callback_query(F.data == 'yes', RecordActionsGroup.deleting_record)
async def delete_record_yes(callback: types.CallbackQuery, state: FSMContext, db: Database) -> None:
    user_data = await state.get_data()

    async with db.session.begin():
        await db.record.delete(Record.id == user_data['record_id'])

    await callback.message.answer('Запись успешно удалена ✅')
    await state.set_state(MainGroup.viewing_storage)

    await callback.answer()


@router.callback_query(F.data == 'no', RecordActionsGroup.deleting_record)
async def delete_record_no(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer('Удаление записи отменено ❌')
    await state.set_state(MainGroup.viewing_record)

    await callback.answer()
