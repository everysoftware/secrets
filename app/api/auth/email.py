import email

from app.core.config import cfg
from app.core.models import User


def thank_you(user: User) -> str:
    template = email.message.EmailMessage()
    template['Subject'] = "Добро пожаловать в Secrets!"
    template['From'] = cfg.smtp.sender
    template['To'] = user.email

    template.set_content(
        '<div style="font-family: Arial, sans-serif; color: #333;">'
        f'<h1 style="color: #48a999;">Здравствуйте, {user.first_name}!</h1>'
        '<p>Благодарим вас за регистрацию в Secrets, вашем быстром и надежном менеджере паролей. '
        'Мы рады приветствовать вас в нашем сообществе!</p>'
        '<p>С Secrets вы можете быть уверены, что ваши пароли и '
        'другие конфиденциальные данные хранятся в безопасности.</p>'
        '<p>Если у вас возникнут вопросы или предложения, не стесняйтесь обращаться к нам.</p>'
        '<p style="color: #48a999;">С уважением,</p>'
        '<p style="color: #48a999;">Команда Secrets</p>'
        '</div>',
        subtype='html'
    )
    return template.as_string()
