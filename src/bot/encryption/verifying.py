import hashlib
import os


class Verifying:
    @classmethod
    def generate_salt(cls) -> bytes:
        return os.urandom(16)

    @classmethod
    def get_hash(
            cls,
            data: str,
            salt: bytes) -> str:
        data_with_salt = data.encode('utf-8') + salt

        hashed_password = hashlib.sha256(data_with_salt).hexdigest()

        return hashed_password

    @classmethod
    def verify(
            cls,
            data: str,
            data_hash: str,
            salt: bytes
    ) -> bool:
        return cls.get_hash(data, salt) == data_hash
