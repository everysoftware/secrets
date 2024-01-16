from domain.user import BaseUserRepository
from infrastructure.base import SARepository
from .models import User


class UserRepository(BaseUserRepository, SARepository):
    model = User
