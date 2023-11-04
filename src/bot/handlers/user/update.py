from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.bot.encryption import Encryption
from src.bot.encryption import Verifying
from src.bot.fsm import MainGroup
from src.bot.fsm import ProfileMasterEditingGroup
from src.bot.fsm import ProfilePasswordEditingGroup
from src.bot.handlers.user.confirmation import send_confirmation_request
from src.bot.utils.forwarding import redirects
from src.bot.utils.messages import Interactive
from src.db import Database
from src.db.models import AuthData
from src.db.models import Record

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
        auth_data.account_password = Verifying.get_hash(text, auth_data.salt)
        await db.auth_data.merge(auth_data)

    await Interactive.finish(
        message, state,
        new_state=MainGroup.viewing_profile,
        text='Пароль успешно изменён ✅'
    )


@router.message(MainGroup.viewing_profile, F.text == 'Сменить мастер-пароль 🗝')
async def update_master_confirmation(message: types.Message, state: FSMContext) -> None:
    await send_confirmation_request(message, state, type_new_master, save_master=True)


@redirects.register_redirect
async def type_new_master(message: types.Message, state: FSMContext) -> None:
    await Interactive.start(
        message, state,
        new_state=ProfileMasterEditingGroup.typing_new_password,
        text='Введи новый мастер-пароль ⬇️'
    )


@router.message(ProfileMasterEditingGroup.typing_new_password)
async def update_master(message: types.Message, state: FSMContext, db: Database) -> None:
    new_master = message.text
    user_data = await state.get_data()

    async with db.session.begin():
        user = await db.user.get(message.from_user.id)
        auth_data: AuthData = user.auth_data
        auth_data.master_password = Verifying.get_hash(new_master, auth_data.salt)
        await db.auth_data.merge(auth_data)

        for record in user.records:
            record: Record
            old_salt = record.salt
            new_salt = Encryption.generate_salt()
            old_password = Encryption.decrypt(record.password_, user_data['master'], old_salt)
            new_password = Encryption.encrypt(old_password, new_master, new_salt)
            old_username = Encryption.decrypt(record.username, user_data['master'], old_salt)
            new_username = Encryption.encrypt(old_username, new_master, new_salt)

            record.salt = new_salt
            record.password_ = new_password
            record.username = new_username

            await db.record.merge(record)

    await Interactive.finish(
        message, state,
        user_data=user_data,
        new_state=MainGroup.viewing_profile,
        text='Мастер-пароль успешно изменён ✅'
    )
