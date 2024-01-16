import abc


class BaseEncryption(abc.ABC):
    @abc.abstractmethod
    def generate_key(self) -> str:
        pass

    @abc.abstractmethod
    def encrypt(self, data: str, key: str) -> str:
        pass

    @abc.abstractmethod
    def decrypt(self, encrypted_data: str, key: str) -> str:
        pass
