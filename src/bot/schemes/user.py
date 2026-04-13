import datetime

from pydantic import computed_field

from src.db.enums import UserRole

from .base import Base


class User(Base):
    id: int
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    role: UserRole
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @computed_field
    @property
    def display_name(self) -> str:
        if self.first_name is not None and self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        return f"{self.first_name}"

    def html(self) -> str:
        result = (
            "<b>{display_name}</b>\n\n"
            "👨 Имя пользователя: @{username}\n"
            "🟢 Роль: {role}\n"
            "🌍 Язык: {language_code}\n"
            "📅 Зарегистрирован: {created_at}\n"
            "🔢 ID: {id}"
        ).format(**self.dump())

        return result

    def welcome(self) -> str:
        match self.role:
            case UserRole.GUEST:
                return (
                    "Добро пожаловать! Я бот, который помогает быстро и безопасно управлять паролями! 😊 "
                    "Давайте создадим аккаунт, для этого нажмите на кнопку 👇"
                )
            case UserRole.USER:
                return (
                    "Добро пожаловать, {display_name}! 😊 "
                    "Чтобы войти в аккаунт, введите пароль ⬇️".format(**self.dump())
                )
            case UserRole.ADMIN:
                return (
                    "Добро пожаловать, супер-кот {display_name}! 😊"
                    "Чтобы войти в аккаунт, введите пароль ⬇️".format(**self.dump())
                )
            case _:
                raise ValueError(f"Unknown user role: {self.role}")
