from abc import ABC

from domain.schemes.entities import UserScheme
from domain.schemes.transfer import UserCreate, UserUpdate
from .base import IRepository


class IUserRepository(IRepository, ABC):
    scheme = UserScheme
    create_scheme = UserCreate
    update_scheme = UserUpdate
