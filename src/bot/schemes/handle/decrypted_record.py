from dataclasses import asdict
from html import escape

from src.bot.schemes.models import DecryptedRecord


class DecryptedRecordHandle:
    def __init__(self, record: DecryptedRecord):
        self.record = record

    def html(self) -> str:
        info = {k: escape(v if v else '') for k, v in asdict(self.record).items()}
        result = (
            f'<b>{info["title"]}</b>\n\n'
            f'👨 Имя пользователя: <code>{info["username"]}</code>\n'
            f'🔑 Пароль: <code>{info["password"]}</code>\n'
            f'🔗 Веб-сайт: {info["url"]}\n'
            f'💬 Комментарий: <tg-spoiler>{info["comment"]}</tg-spoiler>\n\n'
        )

        return result
