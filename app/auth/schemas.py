import datetime

from fastapi_users import schemas
from pydantic import EmailStr
from pydantic import Field

from app.schemas import BackendBase


class SUserRead(BackendBase, schemas.BaseUser[int]):
    id: int
    email: EmailStr
    hashed_password: str = Field(exclude=True)
    first_name: str = Field(max_length=32, examples=["John"])
    last_name: str = Field("", max_length=32, examples=["Doe"])
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    created_at: datetime.datetime
    updated_at: datetime.datetime


class SUserCreate(BackendBase, schemas.BaseUserCreate):
    first_name: str = Field(max_length=32, examples=["John"])
    email: EmailStr
    password: str = Field(
        min_length=1,
        max_length=128,
        examples=["Password123!"],
    )
    last_name: str = Field("", max_length=32, examples=["Doe"])


class SUserUpdate(BackendBase, schemas.BaseUserUpdate):
    first_name: str | None = Field(None, max_length=32, examples=["John"])
    last_name: str | None = None
    password: str | None = None
