import abc

from domain.user import UserScheme


class BaseMailTemplates(abc.ABC):
    @abc.abstractmethod
    def welcome(self, user: UserScheme) -> str:
        pass
