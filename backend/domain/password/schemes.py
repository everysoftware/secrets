import datetime

from domain.base.schemes import BaseScheme
from domain.comment.schemes import CommentRead


class PasswordRead(BaseScheme):
    id: int
    owner_id: int
    name: str
    username: str
    password: str
    url: str | None
    comment: CommentRead | None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PasswordCreate(BaseScheme):
    name: str
    username: str
    password: str
    url: str | None = None


class PasswordUpdate(BaseScheme):
    name: str | None
    username: str | None
    password: str | None
    url: str | None = None


class PasswordItem(BaseScheme):
    id: int
    name: str
    url: str | None = None


class PasswordSettings(BaseScheme):
    length: int = 16
    english_letters: bool = True
    digits: bool = True
    special_characters: str = "!@#$%^&*()_+-=[]{};':\",./<>?`~"
