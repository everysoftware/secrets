from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models import Record


class RecordRepo(Repository[Record]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Record, session=session)
