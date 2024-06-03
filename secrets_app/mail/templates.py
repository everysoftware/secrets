from .base import MBase


class MWelcome(MBase):
    """Приветственное письмо."""

    template: str = "welcome.html"
    subject: str = "Добро пожаловать в Secrets!"
