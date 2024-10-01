from fastapi.exceptions import HTTPException
from starlette import status


class NotEnoughRights(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights"
        )
