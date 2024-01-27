from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader

from common.settings import settings
from domain.interfaces import IMailTemplates
from domain.schemes.entities import UserScheme


def base_message(subject: str, user: UserScheme) -> Message:
    msg = MIMEMultipart("alternative")
    msg["From"] = settings.infrastructure.smtp.username
    msg["To"] = user.email
    msg["Subject"] = subject

    return msg


class MailTemplates(IMailTemplates):
    env = Environment(loader=FileSystemLoader("backend/infrastructure/mail/templates"))

    def render(self, template: str, subject: str, user: UserScheme, **kwargs) -> str:
        msg = base_message(subject, user)
        html = self.env.get_template(template).render(user=user, **kwargs)

        msg.attach(MIMEText(html, "html"))

        return msg.as_string()

    def welcome(self, user: UserScheme) -> str:
        return self.render("welcome.html", "Добро пожаловать в Secrets!", user)


mail_templates = MailTemplates()
