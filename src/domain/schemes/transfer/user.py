import string

from fastapi_users import schemas
from pydantic import field_validator, EmailStr

from domain.schemes.entities.user import (
    first_name_field,
    last_name_field,
    password_field,
)


class UserCreate(schemas.BaseUserCreate):
    first_name: first_name_field
    last_name: last_name_field
    email: EmailStr
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


class UserUpdate(schemas.BaseUserUpdate):
    first_name: first_name_field | None = None
    last_name: last_name_field | None = None
    password: password_field | None = None
