from app.auth.schemas import SUser
from app.core.uow import UOW
from app.passwords.service import PasswordService


class Gateway:
    # Services
    user: SUser
    passwords: PasswordService

    def __init__(self, uow: UOW, user: SUser):
        self.uow = uow
        self.user = user

        self.passwords = PasswordService(uow, self.user)
