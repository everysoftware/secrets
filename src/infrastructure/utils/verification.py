import base64
import hashlib
import os

from domain.interfaces.verification import IVerification


class SHA256Verification(IVerification):
    def generate_salt(self) -> str:
        return base64.b64encode(os.urandom(16)).decode("utf-8")

    def compute_hash(self, data: str, salt: str | None = None) -> str:
        if salt is None:
            salt = self.generate_salt()

        salt_bytes = base64.b64decode(salt)
        data_bytes = data.encode("utf-8") + salt_bytes

        hashed_data = hashlib.sha256(data_bytes).hexdigest()
        salt_str = base64.b64encode(salt_bytes).decode("utf-8")

        return f"{salt_str}:{hashed_data}"

    def verify_data(self, data: str, computed_hash: str) -> bool:
        salt, saved_hash = computed_hash.split(":")

        return self.compute_hash(data, salt) == computed_hash


sha256 = SHA256Verification()
