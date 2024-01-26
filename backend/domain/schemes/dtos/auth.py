from pydantic import Field

from domain.schemes.base import BaseScheme


class TwoFALogin(BaseScheme):
    one_time_password: str = Field(min_length=6, max_length=6, examples=["123456"])
