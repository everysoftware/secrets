from .client import send_email_message
from .templates import MailTemplates, mail_templates

__all__ = [
    "send_email_message",
    "MailTemplates",
    "mail_templates",
]
