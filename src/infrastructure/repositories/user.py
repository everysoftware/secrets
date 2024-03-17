from src.infrastructure.models import UserOrm
from .base import SARepository


class UserRepository(SARepository[UserOrm]):
    model = UserOrm
