import string

import pytest

from application.utils import generate_password


@pytest.mark.parametrize("length", [16, 32, 0, 1])
def test_generate_password(length: int):
    special = "!\"#$%&'()<>*+,-./:;=?@[\\]^_`{|}~"
    password = generate_password(length, special)

    assert isinstance(password, str)
    assert len(password) == length

    characters = string.ascii_letters + string.digits + special
    for char in password:
        assert char in characters
