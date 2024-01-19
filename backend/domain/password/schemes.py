from typing import Annotated

from pydantic import AnyUrl, Field

from domain.base.schemes import BaseScheme, created_at_field, updated_at_field

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


class PasswordBase(BaseScheme):
    name: name_field
    username: username_field
    password: password_field
    url: url_field
    comment: comment_field


class PasswordScheme(PasswordBase):
    id: int
    owner_id: int
    created_at: created_at_field
    updated_at: updated_at_field


class PasswordCreate(PasswordBase):
    pass


class PasswordUpdate(PasswordBase):
    name: name_field | None = None
    username: username_field | None = None
    password: password_field | None = None
    url: url_field | None = None
    comment: comment_field | None = None


class PasswordItem(BaseScheme):
    id: int
    name: name_field
    username: username_field


class PasswordSettings(BaseScheme):
    length: int = 16
    english_letters: bool = True
    digits: bool = True
    special_characters: str = "!@#$%^&*()_+-=[]{};':\",./<>?`~"
