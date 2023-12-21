import pytest

from api.utils import AES
from utils.utils_entities import TEXT_DATA


def test_generate_key():
    key = AES.generate_key()

    assert isinstance(key, bytes)
    assert len(key) == 32


@pytest.mark.parametrize(
    "data",
    TEXT_DATA
)
def test_encrypt_decrypt(data):
    key = AES.generate_key()
    encrypted_data = AES.encrypt(data, key)
    decrypted_data = AES.decrypt(encrypted_data, key)

    assert decrypted_data == data


@pytest.mark.parametrize(
    "data",
    TEXT_DATA
)
def test_decrypt_with_wrong_key(data):
    key1 = AES.generate_key()
    key2 = AES.generate_key()
    encrypted_data = AES.encrypt(data, key1)

    with pytest.raises(ValueError):
        AES.decrypt(encrypted_data, key2)
