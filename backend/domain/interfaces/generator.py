from abc import ABC, abstractmethod

from domain.schemes.dtos.password import PasswordSettings


class IPasswordGenerator(ABC):
    @abstractmethod
    def generate(self, settings: PasswordSettings) -> str:
        pass
