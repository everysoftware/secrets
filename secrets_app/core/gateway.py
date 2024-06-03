from secrets_app.auth.schemas import SUser
from secrets_app.core.uow import UOW
from secrets_app.passwords.service import PasswordService


class UnauthorizedGateway:
    """
    Provides access to application core without authentication.
    """

    def __init__(self, uow: UOW):
        self.uow = uow


class Gateway(UnauthorizedGateway):
    """
    Provides access to application core.

    e.g.::

        async def get_user(
            email: str, gateway: Annotated[ServiceGateway, Depends(get_gateway)]
        ) -> None:
            user = await gateway.users.get_by_email(str)
            return user


        async def handler(message: types.Message, gateway: ServiceGateway) -> None:
            user = await gateway.users.get_by_email(message.text)
            await message.answer(user.model_dump_json())
    """  # noqa: E501

    # User info
    user: SUser

    # Infrastructure
    # ...

    # Services
    passwords: PasswordService

    def __init__(self, uow: UOW, user: SUser):
        self.user = user

        self.passwords = PasswordService(uow, self.user)
        super().__init__(uow)
