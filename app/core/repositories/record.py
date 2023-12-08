from sqlalchemy.ext.asyncio import AsyncSession

from .base import Repository
from ..models import Record


class RecordRepo(Repository[Record]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Record, session=session)

    # @staticmethod
    # def decrypt(record: Record, master: str) -> DecryptedRecord:
    #     return DecryptedRecord(
    #         id=record.id,
    #         title=record.title,
    #         username=Encryption.decrypt(record.username, master, record.salt),
    #         password=Encryption.decrypt(record.password, master, record.salt),
    #         url=record.url,
    #         comment=record.comment.text if record.comment else None,
    #         created_at=record.created_at,
    #         updated_at=record.updated_at,
    #     )
