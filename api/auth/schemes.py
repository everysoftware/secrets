import datetime
import enum
from html import escape as e

from pydantic import BaseModel, ConfigDict

from services.db.enums import UserRole


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    def dump(self):
        dump = self.model_dump()

        for key, value in dump.items():
            if value is None:
                dump[key] = "нет"
            elif isinstance(value, datetime.datetime):
                dump[key] = value.strftime("%d-%m-%Y %H:%M")
            elif isinstance(value, str):
                dump[key] = e(value)
            elif isinstance(value, enum.Enum):
                dump[key] = value.name

        return dump


class DecryptedRecord(Base):
    id: int
    title: str
    username: str
    password: str
    url: str | None
    comment: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def html(self) -> str:
        result = (
            "<b>Пароль {title}</b>\n\n"
            "👨 Имя пользователя: <code>{username}</code>\n"
            "🔑 Пароль: <code>{password}</code>\n"
            "🔗 Веб-сайт: {url}\n"
            "💬 Комментарий: {comment}\n"
            "📅 Создан: {created_at}\n"
            "📅 Изменён: {updated_at}\n"
            "🔢 ID: {id}"
        ).format(**self.dump())

        return result


class User(Base):
    id: int
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    role: UserRole
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def html(self) -> str:
        result = (
            "<b>{first_name} {last_name}</b>\n\n"
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
                return "Добро пожаловать! Я бот, который помогает быстро и безопасно управлять паролями! 😊 "
            case UserRole.USER:
                return "Добро пожаловать, {first_name} {last_name}! 😊 ".format(
                    **self.dump()
                )
            case UserRole.ADMIN:
                return "Добро пожаловать, супер-кот {first_name} {last_name}! 😊".format(
                    **self.dump()
                )
            case _:
                raise ValueError(f"Unknown user role: {self.role}")
