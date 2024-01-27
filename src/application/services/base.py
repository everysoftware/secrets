from abc import ABC

from infrastructure.utils import UnitOfWork


class Service(ABC):
    uow: UnitOfWork

    def __init__(self, uow: UnitOfWork):
        self.uow = uow
