from fastapi import Depends

from application.password import PasswordService
from domain.password import PasswordRead
from infrastructure import User
from interfaces.rest.auth.dependencies import verified_user
from interfaces.rest.dependencies import password_service
from interfaces.rest.exceptions import NotEnoughRights
from interfaces.rest.password.exceptions import PasswordNotFound


async def valid_password(
    item_id: int,
    user: User = Depends(verified_user),
    service: PasswordService = Depends(password_service),
) -> PasswordRead:
    password = await service.get(item_id)

    if not password:
        raise PasswordNotFound()

    if password.owner_id != user.id and not user.is_superuser:
        raise NotEnoughRights()

    return password
