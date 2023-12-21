import pytest

from api.utils import SHA256
from utils.utils_entities import TEXT_DATA


@pytest.mark.parametrize(
    "data",
    TEXT_DATA
)
def test_hash_with_salt(data):
    hashed_data = SHA256.hash_with_salt(data)

    assert isinstance(hashed_data, str)
    assert ":" in hashed_data


@pytest.mark.parametrize(
    "data",
    TEXT_DATA
)
def test_verify(data):
    hashed_data = SHA256.hash_with_salt(data)

    assert SHA256.verify(data, hashed_data)


@pytest.mark.parametrize(
    "data",
    TEXT_DATA
)
def test_verify_with_wrong_data(data):
    wrong_data = "wrong_data"
    hashed_data = SHA256.hash_with_salt(data)

    assert not SHA256.verify(wrong_data, hashed_data)
