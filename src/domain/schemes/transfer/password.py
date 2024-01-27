from domain.schemes.base import BaseScheme, created_at_field, updated_at_field
from domain.schemes.entities.password import (
    name_field,
    username_field,
    password_field,
    url_field,
    comment_field,
)


class EncryptedPassword(BaseScheme):
    id: int
    user_id: int
    name: name_field
    username: str
    password: str
    url: url_field
    comment: comment_field
    created_at: created_at_field
    updated_at: updated_at_field


class PasswordCreate(BaseScheme):
    name: name_field
    username: username_field
    password: password_field
    url: url_field
    comment: comment_field


class PasswordUpdate(BaseScheme):
    name: name_field | None = None
    username: username_field | None = None
    password: password_field | None = None
    url: url_field | None = None
    comment: comment_field | None = None


class PasswordItem(BaseScheme):
    id: int
    name: name_field
    username: username_field
    url: url_field


class PasswordSettings(BaseScheme):
    length: int = 16
    english_letters: bool = True
    digits: bool = True
    special_characters: str = "!@#$%^&*()_+-=[]{};':\",./<>?`~"
