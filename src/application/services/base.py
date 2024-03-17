from src.infrastructure.db import UnitOfWork


class Service:
    uow: UnitOfWork

    def __init__(self, uow: UnitOfWork):
        self.uow = uow
