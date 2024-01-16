import datetime

from domain.base.schemes import BaseScheme


class CommentCreate(BaseScheme):
    password_id: int
    text: str


class CommentRead(BaseScheme):
    password_id: int
    text: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class CommentUpdate(BaseScheme):
    text: str | None
