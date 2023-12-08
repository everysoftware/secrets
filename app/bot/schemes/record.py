import datetime

from .base import Base


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
