import secrets
import string


def generate_password(length: int = 16) -> str:
    punctuation = "!\"#$%&'()<>*+,-./:;=?@[\\]^_`{|}~"
    characters = string.ascii_letters + string.digits + punctuation
    password = "".join(secrets.choice(characters) for _ in range(length))
    return password
