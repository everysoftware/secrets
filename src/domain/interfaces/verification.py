from abc import ABC, abstractmethod


class IVerification(ABC):
    @abstractmethod
    def generate_salt(self) -> str:
        pass

    @abstractmethod
    def compute_hash(self, data: str, salt: str | None = None) -> str:
        pass

    @abstractmethod
    def verify_data(self, data: str, computed_hash: str) -> bool:
        pass
