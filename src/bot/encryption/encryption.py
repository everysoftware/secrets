import hashlib
import os
from typing import Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encrypt_data_(data: bytes, master_password: bytes, salt: bytes) -> bytes:
    # Генерация ключа из мастер-пароля с помощью PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt,
        iterations=100000,  # количество итераций хеширования
        backend=default_backend(),
        length=32
    )
    key = kdf.derive(master_password)

    # Генерация случайного инициализирующего вектора
    iv = os.urandom(16)

    # Создание объекта AES-256-CTR
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Шифрование данных
    ciphertext = encryptor.update(data) + encryptor.finalize()

    # Возвращение инициализирующего вектора и зашифрованных данных
    return iv + ciphertext


def decrypt_data_(data: bytes, master_password: bytes, salt: bytes) -> bytes:
    # Генерация ключа из мастер-пароля с помощью PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt,
        iterations=100000,
        backend=default_backend(),
        length=32
    )
    key = kdf.derive(master_password)

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


def encrypt_data(data: str, master: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
    if salt is None:
        salt = os.urandom(16)
    encrypted_password = encrypt_data_(
        data.encode('utf-8'),
        master.encode('utf-8'),
        salt
    )

    return encrypted_password, salt


def decrypt_data(data: bytes, master: str, salt: bytes) -> str:
    decrypted_password = decrypt_data_(
        data,
        master.encode('utf-8'),
        salt
    )
    return decrypted_password.decode('utf-8')


def hash_data(data: str, salt: Optional[bytes] = None) -> tuple[str, bytes]:
    if salt is None:
        salt = os.urandom(16)  # Генерация случайной соли, если она не предоставлена

    # Конкатенация пароля и соли
    data_with_salt = data.encode('utf-8') + salt

    # Хеширование методом SHA256
    hashed_password = hashlib.sha256(data_with_salt).hexdigest()

    return hashed_password, salt


def verify_data(data: str, data_hash: str, salt: bytes) -> bool:
    temp, _ = hash_data(data, salt)
    return temp == data_hash
