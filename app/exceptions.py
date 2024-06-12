from enum import StrEnum

from fastapi.exceptions import RequestValidationError, HTTPException
from starlette import status


class AppException(Exception):
    pass


class CustomValidationError(RequestValidationError):
    def __init__(self, loc: list[str], msg: str):
        super().__init__([{"loc": loc, "msg": msg, "type": "custom"}])


class ErrorCode(StrEnum):
    pass


class NotEnoughRights(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights"
        )
