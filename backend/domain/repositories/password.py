from abc import ABC

from domain.schemes import PasswordScheme
from domain.schemes.dtos import PasswordCreate, PasswordUpdate
from .base import IRepository


class IPasswordRepository(IRepository, ABC):
    scheme = PasswordScheme
    create_scheme = PasswordCreate
    update_scheme = PasswordUpdate
