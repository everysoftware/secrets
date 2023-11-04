import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Encryption:
    @classmethod
    def _derive_key(
            cls,
            master: bytes,
            salt: bytes,
    ) -> bytes:
        """Генерация ключа из мастер-пароля с помощью PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            salt=salt,
            iterations=100000,  # количество итераций хеширования
            backend=default_backend(),
            length=32
        )
        return kdf.derive(master)

    @classmethod
    def _encrypt(
            cls,
            data: bytes,
            master: bytes,
            salt: bytes
    ) -> bytes:
        key = cls._derive_key(master, salt)

        # Генерация случайного инициализирующего вектора
        iv = os.urandom(16)

        # Создание объекта AES-256-CTR
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Шифрование данных
        ciphertext = encryptor.update(data) + encryptor.finalize()

        # Возвращение инициализирующего вектора и зашифрованных данных
        return iv + ciphertext

    @classmethod
    def _decrypt(
            cls,
            data: bytes,
            master: bytes,
            salt: bytes
    ) -> bytes:
        key = cls._derive_key(master, salt)

        # Извлечение инициализирующего вектора
        iv = data[:16]
        ciphertext = data[16:]

        # Создание объекта AES-256-CTR
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Расшифровка данных
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Возвращение расшифрованных данных
        return plaintext

    @classmethod
    def generate_salt(cls) -> bytes:
        return os.urandom(16)

    @classmethod
    def encrypt(
            cls,
            data: str,
            master: str,
            salt: bytes
    ) -> bytes:
        return cls._encrypt(
            data.encode('utf-8'),
            master.encode('utf-8'),
            salt
        )

    @classmethod
    def decrypt(
            cls,
            data: bytes,
            master: str,
            salt: bytes
    ):
        return cls._decrypt(
            data,
            master.encode('utf-8'),
            salt
        ).decode('utf-8')
