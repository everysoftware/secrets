import hashlib
import os
from typing import Optional


class Verifying:
    @classmethod
    def generate_salt(cls) -> bytes:
        return os.urandom(16)

    @classmethod
    def get_hash(
            cls,
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
        return cls.get_hash(data, salt) == data_hash
