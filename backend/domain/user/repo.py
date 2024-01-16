import abc

from domain.base.repo import BaseRepository
from domain.user.schemes import UserRead, UserCreate, UserUpdate


class BaseUserRepository(BaseRepository, abc.ABC):
    read_scheme = UserRead
    create_scheme = UserCreate
    update_scheme = UserUpdate

    @abc.abstractmethod
    def enable_two_fa(self, user: UserRead) -> str:
        ...
