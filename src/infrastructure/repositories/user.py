from domain.repositories import IUserRepository
from infrastructure.models import User
from .base import SARepository


class UserRepository(IUserRepository, SARepository[User]):
    model = User
