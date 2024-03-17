import base64
import hashlib
import os

SALT_SIZE = 16
ENCODING = "utf-8"
SEPARATOR = ":"


def generate_salt() -> str:
    return base64.b64encode(os.urandom(SALT_SIZE)).decode(ENCODING)


def compute_sha256(self, data: str, salt: str | None = None) -> str:
    if salt is None:
        salt = self.generate_salt()

    salt_bytes = base64.b64decode(salt)
    data_bytes = data.encode(ENCODING) + salt_bytes

    hashed_data = hashlib.sha256(data_bytes).hexdigest()
    salt_str = base64.b64encode(salt_bytes).decode(ENCODING)

    return SEPARATOR.join([salt_str, hashed_data])


def verify_sha256(data: str, computed_hash: str) -> bool:
    salt, saved_hash = computed_hash.split(SEPARATOR)

    return compute_sha256(data, salt) == computed_hash
