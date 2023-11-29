import datetime
from html import escape as e

from pydantic import ConfigDict, BaseModel


class DecryptedRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    username: str
    password: str
    url: str | None
    comment: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def html(self) -> str:
        empty = 'нет'
        result = (
            f'<b>Пароль {e(self.title)} (#{self.id})</b>\n\n'
            f'👨 Имя пользователя: <code>{e(self.username)}</code>\n'
            f'🔑 Пароль: <code>{e(self.password)}</code>\n'
            f'🔗 Веб-сайт: {e(self.url) if self.url else empty}\n'
            f'💬 Комментарий: {e(self.comment) if self.comment else empty}\n'
            f'📅 Дата создания: {self.created_at}\n'
            f'📅 Дата обновления: {self.updated_at}\n'
        )

        return result
