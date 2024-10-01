from fastapi import HTTPException, status


class PasswordNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="Password not found"
        )
