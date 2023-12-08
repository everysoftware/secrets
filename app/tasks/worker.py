import email
import smtplib

from app.core.config import cfg
from app.tasks.app import app


@app.task
def send_email(message: str) -> None:
    message = email.message_from_string(message)
    with smtplib.SMTP_SSL(cfg.smtp.host, cfg.smtp.port) as server:
        server.login(cfg.smtp.username, cfg.smtp.password)
        server.send_message(message)
