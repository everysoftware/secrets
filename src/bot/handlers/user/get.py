from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.db import Database
from src.bot.fsm import MainGroup, RecordGroup
from src.bot.keyboards.user import PROFILE_KB

router = Router()


@router.message(MainGroup.viewing_main_menu, F.text == 'Мой профиль 👨')
@router.message(MainGroup.viewing_all_records, F.text == 'Мой профиль 👨')
@router.message(RecordGroup.viewing_record, F.text == 'Мой профиль 👨')
async def show_user(message: types.Message, state: FSMContext, db: Database) -> None:
    async with db.session.begin():
        user = await db.user.get(message.from_user.id)

    await message.answer(
        f'Пользователь {user.first_name} {user.last_name} (#{user.id})\n\n'
        f'Имя пользователя: @{user.username}\n'
        f'Язык: {user.language_code}\n'
        f'Дата регистрации: {user.created_at}',
        reply_markup=PROFILE_KB
    )
    await state.set_state(MainGroup.viewing_profile)
