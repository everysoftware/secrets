from abc import ABC, abstractmethod

from domain.schemes import UserScheme


class IMailTemplates(ABC):
    @abstractmethod
    def welcome(self, user: UserScheme) -> str:
        pass
