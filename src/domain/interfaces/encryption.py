from abc import ABC, abstractmethod


class IEncryption(ABC):
    @abstractmethod
    def generate_key(self) -> str:
        pass

    @abstractmethod
    def encrypt(self, data: str, key: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, encrypted_data: str, key: str) -> str:
        pass
