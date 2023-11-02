from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models import User, Record


class RecordRepo(Repository[Record]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Record, session=session)

    def new(
            self,
            user: User,
            title: str,
            username: bytes,
            password: bytes,
            salt: bytes
    ) -> Record:
        new_record = Record(
            user=user,
            title=title,
            username=username,
            password_=password,
            salt=salt,
        )
        self.session.add(new_record)
        return new_record
