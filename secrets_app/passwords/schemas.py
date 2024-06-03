from pydantic import Field

from secrets_app.schemas import MainModel, Page
from secrets_app.skeleton import EntityModel


class SPasswordBase(MainModel):
    title: str = Field(min_length=1, max_length=128, examples=["Facebook"])
    username: str = Field(
        min_length=1,
        max_length=128,
        examples=["user@example.com"],
    )
    url: str = Field("", max_length=256, examples=["https://example.com"])
    note: str = Field("", max_length=256, examples=["Sample comment"])


class SPassword(EntityModel, SPasswordBase):
    user_id: int
    password: str = Field(min_length=1, max_length=128, examples=["qwerty123"])


class SPasswordCreate(SPasswordBase):
    password: str = Field(min_length=1, max_length=128, examples=["qwerty123"])


class SPasswordUpdate(SPasswordCreate):
    pass


class SPasswordItem(SPasswordBase):
    id: int


class SPasswordPage(Page[SPasswordItem]):
    pass


# Encryption
class SPasswordEncrypted(SPassword):
    username: str
    password: str


class SPasswordCreateEncrypted(SPasswordCreate):
    username: str
    password: str


class SPasswordUpdateEncrypted(SPasswordUpdate):
    username: str | None = None
    password: str | None = None
