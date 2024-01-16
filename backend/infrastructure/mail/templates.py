from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader

from domain.mail.templates import BaseMailTemplates
from domain.user import UserRead
from infrastructure.config import infrastructure_settings


def base_message(subject: str, user: UserRead) -> Message:
    msg = MIMEMultipart("alternative")
    msg["From"] = infrastructure_settings.smtp.username
    msg["To"] = user.email
    msg["Subject"] = subject

    return msg


class MailTemplates(BaseMailTemplates):
    env = Environment(loader=FileSystemLoader("backend/domain/mail/templates"))

    def render(self, template: str, subject: str, user: UserRead, **kwargs) -> str:
        msg = base_message(subject, user)
        html = self.env.get_template(template).render(user=user, **kwargs)

        msg.attach(MIMEText(html, "html"))

        return msg.as_string()

    def welcome(self, user: UserRead) -> str:
        return self.render("welcome.html", "Добро пожаловать в Secrets!", user)


mail_templates = MailTemplates()
