from abc import ABC, abstractmethod

from domain.schemes.entities import UserScheme


class IMailTemplates(ABC):
    @abstractmethod
    def welcome(self, user: UserScheme) -> str:
        pass
