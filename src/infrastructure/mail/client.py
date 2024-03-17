import smtplib
from email.message import Message

from src.infrastructure.config import settings


def smtp_session() -> smtplib.SMTP_SSL:
    """Создание сессии SMTP."""
    server = smtplib.SMTP_SSL(settings.smtp.host, settings.smtp.port)
    server.login(settings.smtp.username, settings.smtp.password)
    return server


def send_email_message(message: Message) -> None:
    """Отправка сообщения."""
    with smtp_session() as server:
        server.send_message(message)
