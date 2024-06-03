import smtplib
from email.message import Message

from secrets_app.settings import settings


def smtp_session() -> smtplib.SMTP_SSL:
    server = smtplib.SMTP_SSL(settings.smtp.host, settings.smtp.port)
    server.login(settings.smtp.username, settings.smtp.password.get_secret_value())

    return server


def send_email_message(message: Message) -> None:
    with smtp_session() as server:
        server.send_message(message)
