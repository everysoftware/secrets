import datetime
import string

from fastapi_users import schemas
from pydantic import EmailStr, field_validator
from pydantic import Field


class SUser(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    hashed_password: str = Field(exclude=True)
    first_name: str = Field(min_length=1, max_length=32, examples=["John"])
    last_name: str = Field("", min_length=1, max_length=32, examples=["Doe"])
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    created_at: datetime.datetime
    updated_at: datetime.datetime


class SUserCreate(schemas.BaseUserCreate):
    first_name: str = Field(min_length=1, max_length=32, examples=["John"])
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Пароль должен содержать не менее 8 символов, включая хотя бы одну заглавную букву, "
        "одну строчную букву, одну цифру и один специальный символ.",
        examples=["Password123!"],
    )
    last_name: str = Field("", min_length=1, max_length=32, examples=["Doe"])

    @field_validator("password")  # noqa
    @classmethod
    def validate_password(cls, password):
        if not any(c.isupper() for c in password):
            raise ValueError(
                "Пароль должен содержать хотя бы одну заглавную букву"
            )
        if not any(c.islower() for c in password):
            raise ValueError(
                "Пароль должен содержать хотя бы одну строчную букву"
            )
        if not any(c.isdigit() for c in password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not any(c in string.punctuation for c in password):
            raise ValueError(
                "Пароль должен содержать хотя бы один специальный символ"
            )

        return password


class SUserUpdate(schemas.BaseUserUpdate):
    first_name: str | None = Field(
        None, min_length=1, max_length=32, examples=["John"]
    )
    last_name: str | None = None
    password: str | None = None
