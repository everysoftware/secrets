from abc import ABC

from domain.schemes import UserScheme
from domain.schemes.dtos import UserCreate, UserUpdate
from .base import IRepository


class IUserRepository(IRepository, ABC):
    scheme = UserScheme
    create_scheme = UserCreate
    update_scheme = UserUpdate
