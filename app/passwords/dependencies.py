from app.auth.dependencies import MeDep
from app.dependencies import GWDep
from app.exceptions import NotEnoughRights
from app.passwords.exceptions import PasswordNotFound
from app.passwords.schemas import SPassword


async def valid_password(
    password_id: int,
    user: MeDep,
    gw: GWDep,
) -> SPassword:
    password = await gw.passwords.get(password_id)

    if password is None:
        raise PasswordNotFound()

    if password.user_id != user.id and not user.is_superuser:
        raise NotEnoughRights()

    return password
