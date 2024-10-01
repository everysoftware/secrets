from typing import Annotated

from fastapi import Depends

from app.auth.dependencies import MeDep
from app.exceptions import NotEnoughRights
from app.passwords.exceptions import PasswordNotFound
from app.passwords.schemas import SPasswordRead
from app.passwords.service import PasswordService

PasswordServiceDep = Annotated[PasswordService, Depends()]


async def valid_password(
    service: PasswordServiceDep,
    user: MeDep,
    password_id: int,
) -> SPasswordRead:
    password = await service.get(password_id)
    if password is None:
        raise PasswordNotFound()
    if password.user_id != user.id and not user.is_superuser:
        raise NotEnoughRights()
    return password
