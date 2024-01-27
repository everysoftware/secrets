import email

from infrastructure.mail import send_email_message
from infrastructure.tasks.app import app


@app.task
def send_email(message: str) -> None:
    send_email_message(email.message_from_string(message))
