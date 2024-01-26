from fastapi import Depends

from application.services import PasswordService
from domain.schemes import PasswordScheme
from infrastructure.models import User
from .auth import verified_user
from .general import password_service
from ..exceptions import PasswordNotFound, NotEnoughRights


async def valid_password(
    item_id: int,
    user: User = Depends(verified_user),
    service: PasswordService = Depends(password_service),
) -> PasswordScheme:
    password = await service.get(item_id)

    if not password:
        raise PasswordNotFound()

    if password.user_id != user.id and not user.is_superuser:
        raise NotEnoughRights()

    return password
