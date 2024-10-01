from pydantic import Field

from app.db.schemas import Page
from app.db.schemas import TimestampModel, IDModel
from app.schemas import BackendBase


class SPasswordBase(BackendBase):
    name: str = Field(min_length=1, max_length=128, examples=["Facebook"])
    url: str = Field("", max_length=256, examples=["https://example.com"])
    note: str = Field("", max_length=256, examples=["Sample comment"])


class SPasswordDB(SPasswordBase, IDModel, TimestampModel):
    user_id: int
    encrypted_username: str
    encrypted_password: str


class SPasswordRead(SPasswordBase, IDModel, TimestampModel):
    user_id: int
    username: str
    password: str


class SPasswordCreate(SPasswordBase):
    username: str = Field(
        min_length=1, max_length=128, examples=["user@example.com"]
    )
    password: str = Field(min_length=1, max_length=128, examples=["qwerty123"])


class SPasswordUpdate(BackendBase):
    username: str | None = Field(
        None, min_length=1, max_length=128, examples=["user@example.com"]
    )
    password: str | None = Field(
        None, min_length=1, max_length=128, examples=["qwerty123"]
    )
    name: str | None = Field(
        None, min_length=1, max_length=128, examples=["Facebook"]
    )
    url: str | None = Field(
        None, max_length=256, examples=["https://example.com"]
    )
    note: str | None = Field(None, max_length=256, examples=["Sample comment"])


class SPasswordItem(SPasswordRead):
    password: str = Field(exclude=True)


class SPasswordPage(Page[SPasswordItem]):
    pass
