from secrets_app.auth.dependencies import MeDep
from secrets_app.dependencies import GWDep
from secrets_app.exceptions import NotEnoughRights
from secrets_app.passwords.exceptions import PasswordNotFound
from secrets_app.passwords.schemas import SPassword


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
