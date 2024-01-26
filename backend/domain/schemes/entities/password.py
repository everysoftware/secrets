from typing import Annotated

from pydantic import Field

from domain.schemes import BaseScheme
from domain.schemes.base import created_at_field, updated_at_field

name_field = Annotated[
    str, Field(min_length=1, max_length=128, examples=["Facebook", "Google", "GitHub"])
]
username_field = Annotated[
    str,
    Field(
        min_length=1,
        max_length=128,
        examples=["user@example.com", "+380501234567", "nickname"],
    ),
]
password_field = Annotated[
    str,
    Field(
        min_length=1, max_length=128, examples=["qwerty123", "12345678", "Password123!"]
    ),
]
comment_field = Annotated[
    str | None, Field(None, min_length=1, max_length=256, examples=["Sample comment"])
]
url_field = Annotated[
    str | None, Field(None, max_length=256, examples=["https://example.com"])
]


class PasswordScheme(BaseScheme):
    id: int
    user_id: int
    name: name_field
    username: username_field
    password: password_field
    url: url_field
    comment: comment_field
    created_at: created_at_field
    updated_at: updated_at_field
