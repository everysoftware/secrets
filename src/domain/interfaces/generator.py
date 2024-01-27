from abc import ABC, abstractmethod

from domain.schemes.transfer.password import PasswordSettings


class IPasswordGenerator(ABC):
    @abstractmethod
    def generate(self, settings: PasswordSettings) -> str:
        pass
