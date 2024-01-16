import abc

from domain.user import UserRead


class BaseMailTemplates(abc.ABC):
    @abc.abstractmethod
    def welcome(self, user: UserRead) -> str:
        pass
