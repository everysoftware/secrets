import secrets
import string


def generate_password(
        length: int = 16, special: str = "!\"#$%&'()<>*+,-./:;=?@[\\]^_`{|}~"
) -> str:
    characters = string.ascii_letters + string.digits + special
    password = "".join(secrets.choice(characters) for _ in range(length))
    return password
