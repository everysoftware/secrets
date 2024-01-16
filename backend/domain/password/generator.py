import abc

from domain.password.schemes import PasswordSettings


class BasePasswordGenerator(abc.ABC):
    @abc.abstractmethod
    def generate(self, settings: PasswordSettings) -> str:
        pass
