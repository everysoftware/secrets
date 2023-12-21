import datetime

from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict

from app.core.enums import UserRole


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    role: UserRole
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    master_password: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None


class TwoFALogin(BaseModel):
    master_password: str

    model_config = ConfigDict(from_attributes=True)
