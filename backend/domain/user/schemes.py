import string
from typing import Annotated

from fastapi_users import schemas
from pydantic import Field, field_validator, EmailStr, Extra

from domain.base import BaseScheme, created_at_field, updated_at_field

first_name_field = Annotated[str, Field(min_length=1, max_length=32, examples=["John"])]
last_name_field = Annotated[str, Field(min_length=1, max_length=32, examples=["Doe"])]
otp_secret_field = Annotated[
    str | None, Field(None, min_length=32, max_length=32, exclude=True)
]
password_field = Annotated[
    str,
    Field(
        min_length=8,
        max_length=128,
        description="Пароль должен содержать не менее 8 символов, включая хотя бы одну заглавную букву, "
        "одну строчную букву, одну цифру и один специальный символ.",
        examples=["Password123!"],
    ),
]


class UserBase(BaseScheme):
    first_name: first_name_field
    last_name: last_name_field


class UserScheme(schemas.BaseUser[int], UserBase):
    is_2fa_enabled: bool = False
    otp_secret: otp_secret_field
    created_at: created_at_field
    updated_at: updated_at_field


class UserCreate(schemas.BaseUserCreate, UserBase):
    password: password_field

    @field_validator("password")
    def validate_password(cls, password):
        if not any(c.isupper() for c in password):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not any(c.islower() for c in password):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        if not any(c.isdigit() for c in password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not any(c in string.punctuation for c in password):
            raise ValueError("Пароль должен содержать хотя бы один специальный символ")
        return password


class UserUpdate(schemas.BaseUserUpdate, UserBase):
    first_name: first_name_field | None = None
    last_name: last_name_field | None = None
    password: password_field | None = None
