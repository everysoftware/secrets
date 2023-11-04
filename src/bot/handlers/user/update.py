from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.encryption import hash_data
from src.bot.fsm import MainGroup
from src.bot.fsm import ProfilePasswordEditingGroup
from src.bot.utils.messages import Interactive
from src.db import Database
from src.db.models import AuthData

router = Router(name='profile_update')


@router.message(MainGroup.viewing_profile, F.text == 'Сменить пароль 🔑')
async def type_old_password(message: types.Message, state: FSMContext) -> None:
    await Interactive.start(
        message, state,
        new_state=ProfilePasswordEditingGroup.typing_old_password,
        text='Введи старый пароль ⬇️'
    )


@router.message(ProfilePasswordEditingGroup.typing_old_password)
async def type_new_password(message: types.Message, state: FSMContext, db: Database) -> None:
    text = message.text

    if not await db.user.authorize(message.from_user.id, text):
        return await Interactive.switch(
            message, state,
            text='Неверный пароль. Введи старый пароль ⬇️'
        )

    await Interactive.switch(
        message, state,
        new_state=ProfilePasswordEditingGroup.typing_new_password,
        text='Введи новый пароль ⬇️'
    )


@router.message(ProfilePasswordEditingGroup.typing_new_password)
async def update_password(message: types.Message, state: FSMContext, db: Database) -> None:
    text = message.text

    async with db.session.begin():
        user = await db.user.get(message.from_user.id)
        auth_data: AuthData = user.auth_data
        auth_data.account_password = hash_data(text, auth_data.salt)[0]
        await db.auth_data.merge(auth_data)

    await Interactive.finish(
        message, state,
        new_state=MainGroup.viewing_profile,
        text='Пароль успешно изменён ✅'
    )


@router.message(MainGroup.viewing_profile, F.text == 'Сменить мастер-пароль 🗝')
async def type_old_master(message: types.Message) -> None:
    await message.answer(
        'Эта функция находится в разработке!',
    )
    # await Interactive.start(
    #     message, state,
    #     new_state=ProfilePasswordEditingGroup.typing_old_password,
    #     text='Введи старый мастер-пароль ⬇️'
    # )
