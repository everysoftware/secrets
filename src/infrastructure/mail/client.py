import smtplib
from email.message import Message

from common.settings import settings


def smtp_session() -> smtplib.SMTP_SSL:
    server = smtplib.SMTP_SSL(
        settings.infrastructure.smtp.host, settings.infrastructure.smtp.port
    )
    server.login(
        settings.infrastructure.smtp.username, settings.infrastructure.smtp.password
    )
    return server


def send_email_message(message: Message) -> None:
    with smtp_session() as server:
        server.send_message(message)
