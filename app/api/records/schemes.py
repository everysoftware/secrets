import datetime

from pydantic import BaseModel, ConfigDict


class CommentRead(BaseModel):
    id: int
    record_id: int
    text: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class RecordRead(BaseModel):
    id: int
    name: str
    username: str
    password: str
    url: str | None
    comment: CommentRead | None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    text: str

    model_config = ConfigDict(from_attributes=True)


class RecordCreate(BaseModel):
    name: str
    username: str
    password: str
    url: str | None = None
    comment: CommentCreate | None = None

    model_config = ConfigDict(from_attributes=True)


class CommentUpdate(BaseModel):
    text: str | None

    model_config = ConfigDict(from_attributes=True)


class RecordUpdate(BaseModel):
    name: str | None
    username: str | None
    password: str | None
    url: str | None = None
    comment: CommentUpdate | None = None

    model_config = ConfigDict(from_attributes=True)


class RecordsRead(BaseModel):
    items: list[RecordRead]
    total: int
    page: int
    pages: int
    per_page: int

    model_config = ConfigDict(from_attributes=True)
