from abc import ABC

from domain.schemes.entities import PasswordScheme
from domain.schemes.transfer import PasswordCreate, PasswordUpdate
from .base import IRepository


class IPasswordRepository(IRepository, ABC):
    scheme = PasswordScheme
    create_scheme = PasswordCreate
    update_scheme = PasswordUpdate
