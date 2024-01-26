from domain.repositories import IPasswordRepository
from infrastructure.models import Password
from .base import SARepository


class PasswordRepository(IPasswordRepository, SARepository[Password]):
    model = Password
