import base64
import hashlib
import os


class SHA256:
    @staticmethod
    def hash_with_salt(data: str, salt: bytes | None = None) -> str:
        if salt is None:
            salt = os.urandom(16)

        data_with_salt = data.encode("utf-8") + salt
        hashed_data = hashlib.sha256(data_with_salt).hexdigest()
        salt_str = base64.b64encode(salt).decode("utf-8")

        return f"{salt_str}:{hashed_data}"

    @classmethod
    def verify(cls, data: str, data_hash: str) -> bool:
        salt_str, saved_hash = data_hash.split(":")
        salt = base64.b64decode(salt_str)

        return cls.hash_with_salt(data, salt) == data_hash
