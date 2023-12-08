import datetime

from pydantic import BaseModel


class CommentRead(BaseModel):
    id: int
    record_id: int
    text: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class RecordRead(BaseModel):
    id: int
    name: str
    username: str
    password: str
    url: str | None
    comment: CommentRead | None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class CommentCreate(BaseModel):
    text: str


class RecordCreate(BaseModel):
    name: str
    username: str
    password: str
    url: str | None = None
    comment: CommentCreate | None = None


class CommentUpdate(BaseModel):
    text: str | None


class RecordUpdate(RecordCreate):
    name: str | None
    username: str | None
    password: str | None
    url: str | None = None
    comment: CommentUpdate | None = None


class RecordsRead(BaseModel):
    items: list[RecordRead]
    total: int
    page: int
    per_page: int
