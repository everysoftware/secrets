import secrets
import string

from domain.password.generator import BasePasswordGenerator
from domain.password.schemes import PasswordSettings


class PasswordGenerator(BasePasswordGenerator):
    def generate(self, settings: PasswordSettings) -> str:
        alphabet = ""

        if settings.english_letters:
            alphabet += string.ascii_letters

        if settings.digits:
            alphabet += string.digits

        alphabet += settings.special_characters

        password = "".join(secrets.choice(alphabet) for _ in range(settings.length))
        return password


password_generator = PasswordGenerator()
