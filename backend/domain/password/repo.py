import abc

from domain.base import Page, Params
from domain.base.repo import BaseRepository
from domain.password.schemes import (
    PasswordRead,
    PasswordCreate,
    PasswordUpdate,
    PasswordItem,
)


class BasePasswordRepository(BaseRepository, abc.ABC):
    read_scheme = PasswordRead
    create_scheme = PasswordCreate
    update_scheme = PasswordUpdate

    @abc.abstractmethod
    async def count(self) -> int:
        ...

    @abc.abstractmethod
    async def search(self, params: Params) -> Page[PasswordItem]:
        ...
