import hashlib
import os
from typing import Optional


class DataVerification:
    @staticmethod
    def generate_salt() -> bytes:
        return os.urandom(16)

    @staticmethod
    def hash(
            data: str,
            salt: Optional[bytes] = None) -> str:
        data_with_salt = data.encode('utf-8')

        if salt:
            data_with_salt += salt

        hashed_password = hashlib.sha256(data_with_salt).hexdigest()

        return hashed_password

    @classmethod
    def verify(
            cls,
            data: str,
            data_hash: str,
            salt: Optional[bytes] = None
    ) -> bool:
        return cls.hash(data, salt) == data_hash
