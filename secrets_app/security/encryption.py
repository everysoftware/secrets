import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY_SIZE = 32
ENCODING = "utf-8"
IV_SIZE = 16
CONTEXT_BLOCK_SIZE = 128
SEPARATOR = ":"


def generate_aes_key() -> str:
    return base64.b64encode(os.urandom(KEY_SIZE)).decode(ENCODING)


def encrypt_aes(data: str, key: str) -> str:
    key_bytes = base64.b64decode(key)
    iv = os.urandom(IV_SIZE)

    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    context = padding.PKCS7(CONTEXT_BLOCK_SIZE).padder()
    padded_data = context.update(data.encode(ENCODING)) + context.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    iv_str = base64.b64encode(iv).decode(ENCODING)
    encrypted_data_str = base64.b64encode(encrypted_data).decode(ENCODING)

    result = SEPARATOR.join([iv_str, encrypted_data_str])

    return result


def decrypt_aes(encrypted_data: str, key: str) -> str:
    key_str = base64.b64decode(key)
    iv_str, encrypted_data_str = encrypted_data.split(SEPARATOR)
    iv = base64.b64decode(iv_str)
    encrypted_bytes = base64.b64decode(encrypted_data_str)

    cipher = Cipher(algorithms.AES(key_str), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_bytes = decryptor.update(encrypted_bytes) + decryptor.finalize()

    context = padding.PKCS7(CONTEXT_BLOCK_SIZE).unpadder()
    decrypted_bytes = context.update(decrypted_bytes) + context.finalize()

    result = decrypted_bytes.decode(ENCODING)

    return result
