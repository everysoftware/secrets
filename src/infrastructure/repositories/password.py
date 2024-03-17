from src.infrastructure.models import PasswordOrm
from .base import SARepository


class PasswordRepository(SARepository[PasswordOrm]):
    model = PasswordOrm
