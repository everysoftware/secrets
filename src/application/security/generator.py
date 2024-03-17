import secrets
import string

from src.domain.schemes import SPasswordGenerate


def generate_password(settings: SPasswordGenerate) -> str:
    alphabet = ""

    if settings.english_letters:
        alphabet += string.ascii_letters

    if settings.digits:
        alphabet += string.digits

    alphabet += settings.special_characters
    password = "".join(secrets.choice(alphabet) for _ in range(settings.length))

    return password
