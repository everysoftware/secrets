import datetime
from html import escape as e

from pydantic import BaseModel, ConfigDict

from src.db.enums import UserRole


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    role: UserRole
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def html(self) -> str:
        empty = 'нет'
        result = (
            f'<b>Пользователь {e(self.first_name)} {e(self.last_name)} (#{self.id})</b>\n\n'
            f'👨 Имя пользователя: @{e(self.username) if self.username else empty}\n'
            f'🟢 Роль: {self.role.name}\n'
            f'🌍 Язык: {e(self.language_code) if self.language_code else empty}\n'
            f'📅 Дата регистрации: {self.created_at}'
        )

        return result
