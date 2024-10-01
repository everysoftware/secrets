from abc import ABC

from app.db.dependencies import UOWDep
from app.db.uow import UOW


class Service(ABC):
    uow: UOW

    def __init__(self, uow: UOWDep):
        self.uow = uow
