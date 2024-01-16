import smtplib
from email.message import Message

from infrastructure.config import infrastructure_settings


def smtp_session() -> smtplib.SMTP_SSL:
    server = smtplib.SMTP_SSL(
        infrastructure_settings.smtp.host, infrastructure_settings.smtp.port
    )
    server.login(
        infrastructure_settings.smtp.username, infrastructure_settings.smtp.password
    )
    return server


def send_email_message(message: Message) -> None:
    with smtp_session() as server:
        server.send_message(message)
