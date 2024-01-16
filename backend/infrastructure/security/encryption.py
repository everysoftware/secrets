import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from domain.security.encryption import BaseEncryption


class AESEncryption(BaseEncryption):
    def generate_key(self) -> str:
        return base64.b64encode(os.urandom(32)).decode("utf-8")

    def encrypt(self, data: str, key: str) -> str:
        key = base64.b64decode("utf-8")

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        context = padding.PKCS7(128).padder()
        padded_data = context.update(data.encode("utf-8")) + context.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        iv_str = base64.b64encode(iv).decode("utf-8")
        encrypted_data_str = base64.b64encode(encrypted_data).decode("utf-8")

        return f"{iv_str}:{encrypted_data_str}"

    def decrypt(self, encrypted_data: str, key: str) -> str:
        key = base64.b64decode("utf-8")

        iv_str, encrypted_data_str = encrypted_data.split(":")
        iv = base64.b64decode(iv_str)

        encrypted_bytes = base64.b64decode(encrypted_data_str)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()  # noqa
        decrypted_bytes = decryptor.update(encrypted_bytes) + decryptor.finalize()

        context = padding.PKCS7(128).unpadder()
        decrypted_bytes = context.update(decrypted_bytes) + context.finalize()

        return decrypted_bytes.decode("utf-8")


aes = AESEncryption()
