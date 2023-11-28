from dataclasses import asdict

from src.bot.schemes.models import DecryptedRecord


class DecryptedRecordHandle:
    def __init__(self, record: DecryptedRecord):
        self.record = record

    def html(self) -> str:
        info = {}
        for k, v in asdict(self.record).items():
            if isinstance(v, str):
                info[k] = v
            elif v is None:
                info[k] = 'нет'

        result = (
            f'<b>Пароль {info["title"]} (#{self.record.id})</b>\n\n'
            f'👨 Имя пользователя: <code>{info["username"]}</code>\n'
            f'🔑 Пароль: <code>{info["password"]}</code>\n'
            f'🔗 Веб-сайт: {info["url"]}\n'
            f'💬 Комментарий: <tg-spoiler>{info["comment"]}</tg-spoiler>\n'
            f'📅 Дата создания: {self.record.created_at}\n'
            f'📅 Дата обновления: {self.record.updated_at}\n'
        )

        return result
