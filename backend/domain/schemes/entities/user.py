from typing import Annotated

from fastapi_users import schemas, models
from pydantic import Field, EmailStr

from domain.schemes.base import created_at_field, updated_at_field, BaseScheme

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


class UserScheme(schemas.BaseUser[int], BaseScheme):
    id: models.ID
    email: EmailStr
    hashed_password: str = Field(exclude=True)
    first_name: first_name_field
    last_name: last_name_field
    is_2fa_enabled: bool = False
    otp_secret: otp_secret_field
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    created_at: created_at_field
    updated_at: updated_at_field
