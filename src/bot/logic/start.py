from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from src.bot.commands import BOT_COMMANDS_STR
from src.bot.fsm import LoginGroup, RegisterGroup
from src.bot.keyboards.auth import REG_KB
from src.bot.schemes import User as UserScheme
from src.db import Database
from src.db.enums import UserRole
from src.db.models import User

from ..middlewares import DatabaseMd
from .main import show_main_menu

router = Router()

router.message.middleware(DatabaseMd())


async def register_if_necessary(message: types.Message, db: Database) -> User:
    async with db.session.begin():
        user = await db.user.get(message.from_user.id)

        if user is None:
            user = db.user.new(
                User(
                    id=message.from_user.id,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                    username=message.from_user.username,
                    language_code=message.from_user.language_code,
                )
            )

    return user


@router.message(Command("start"), default_state)
async def start(message: types.Message, state: FSMContext, db: Database) -> Message:
    user = await register_if_necessary(message, db)
    welcome = UserScheme.model_validate(user).welcome()

    match user.role:
        case UserRole.GUEST:
            message = await message.answer(welcome, reply_markup=REG_KB)
            await state.set_state(RegisterGroup.in_lobby)
        case UserRole.USER | UserRole.ADMIN:
            message = await message.answer(welcome, reply_markup=ReplyKeyboardRemove())
            await state.set_state(LoginGroup.type_password)
        case _:
            raise ValueError(f"Unknown user role: {user.role}")

    return message


@router.message(Command("start"))
async def forward_to_menu(message: types.Message, state: FSMContext) -> None:
    await show_main_menu(message, state)


@router.message(Command("help"))
async def help_handler(message: types.Message) -> Message:
    return await message.answer("<b>Что может бот?</b>\n\n" + BOT_COMMANDS_STR)


@router.message(Command("about"))
async def about(message: types.Message) -> Message:
    return await message.answer(
        "<b>SECRETS</b>\n"
        "Быстрый и безопасный менеджер паролей.\n\n"
        "Made with ❤️ by @ivanstasevich"
    )
