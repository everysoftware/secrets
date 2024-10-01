# Import models for alembic

from app.auth.models import UserOrm
from app.passwords.models import PasswordOrm
from .base import BaseOrm

__all__ = ["BaseOrm", "UserOrm", "PasswordOrm"]
