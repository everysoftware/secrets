import datetime

from fastapi_users import schemas
from pydantic import Field

from domain.base.schemes import BaseScheme


class UserRead(schemas.BaseUser[int], BaseScheme):
    first_name: str
    last_name: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserCreate(schemas.BaseUserCreate, BaseScheme):
    first_name: str
    last_name: str | None = None
    password: str = Field(min_length=8)


class UserUpdate(schemas.BaseUserUpdate, BaseScheme):
    first_name: str | None = None
    last_name: str | None = None


class TwoFALogin(BaseScheme):
    otp: str
