import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class AES:
    @staticmethod
    def generate_key() -> bytes:
        return os.urandom(32)

    @staticmethod
    def encrypt(data: str, key: str | bytes | None = None) -> str:
        if key is None:
            key = AES.generate_key()
        if isinstance(key, str):
            key = key.encode("utf-8")

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        context = padding.PKCS7(128).padder()
        padded_data = context.update(data.encode("utf-8")) + context.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        # Кодируем ключ, iv и зашифрованные данные в base64, чтобы можно было сохранить их в виде строки
        iv_str = base64.b64encode(iv).decode("utf-8")
        encrypted_data_str = base64.b64encode(encrypted_data).decode("utf-8")

        return f"{iv_str}:{encrypted_data_str}"

    @classmethod
    def decrypt(cls, key: str | bytes, encrypted_data: str) -> str:
        if isinstance(key, str):
            key = key.encode("utf-8")

        iv_str, encrypted_data_str = encrypted_data.split(":")
        iv = base64.b64decode(iv_str)
        encrypted_data = base64.b64decode(encrypted_data_str)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        context = padding.PKCS7(128).unpadder()
        data = context.update(decrypted_data) + context.finalize()

        return data.decode("utf-8")
