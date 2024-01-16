import abc


class BaseVerification(abc.ABC):
    @abc.abstractmethod
    def generate_salt(self) -> str:
        pass

    @abc.abstractmethod
    def compute_hash(self, data: str, salt: str | None = None) -> str:
        pass

    @abc.abstractmethod
    def verify_data(self, data: str, computed_hash: str) -> bool:
        pass
