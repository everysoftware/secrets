from typing import Annotated

from pydantic import Field

from .base import SBase, created_at_field, updated_at_field, SPage

title_field = Annotated[
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
note_field = Annotated[str, Field("", max_length=256, examples=["Sample comment"])]
url_field = Annotated[str, Field("", max_length=256, examples=["https://example.com"])]


class SPassword(SBase):
    id: int
    user_id: int
    title: title_field
    username: username_field
    password: password_field
    url: url_field
    note: note_field
    created_at: created_at_field
    updated_at: updated_at_field


class SPasswordEncrypted(SPassword):
    username: str
    password: str


class SPasswordCreate(SBase):
    title: title_field
    username: username_field
    password: password_field
    url: url_field
    note: note_field


class SPasswordCreateEncrypted(SPasswordCreate):
    username: str
    password: str


class SPasswordUpdate(SBase):
    title: title_field | None = None
    username: username_field | None = None
    password: password_field | None = None
    url: url_field = None
    note: note_field = None


class SPasswordUpdateEncrypted(SPasswordUpdate):
    username: str | None = None
    password: str | None = None


class SPasswordItem(SBase):
    id: int
    title: title_field
    username: username_field
    url: url_field


class SPasswordPage(SPage[SPasswordItem]):
    pass


class SPasswordGenerate(SBase):
    length: int = 16
    english_letters: bool = True
    digits: bool = True
    special_characters: str = "!@#$%^&*()_+-=[]{};':\",./<>?`~"
