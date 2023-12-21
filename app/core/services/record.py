from typing import Sequence

from sqlalchemy.orm import joinedload

from app.api.records.schemes import RecordCreate, RecordUpdate
from app.api.utils import AES
from app.core.config import cfg
from app.core.models import Comment, Record, User
from app.core.repositories import RecordRepository


class RecordService:
    repository: RecordRepository

    def __init__(self, repository: RecordRepository, user: User):
        self.repository = repository
        self.user = user

    async def create(self, record: RecordCreate) -> Record:
        db_record = Record(
            user_id=self.user.id,
            name=record.name,
            username=AES.encrypt(record.username, cfg.api.secret_encryption),
            password=AES.encrypt(record.password, cfg.api.secret_encryption),
            url=record.url,
        )

        return await self.repository.create(
            db_record, Comment(**record.comment.model_dump())
        )

    async def get(self, ident: int) -> Record:
        return await self.repository.get(
            ident, options=[joinedload(Record.comment)]  # noqa E501
        )

    async def count(self) -> int:
        return await self.repository.count(self.user.id)

    async def paginate(self, page: int, per_page: int) -> Sequence[Record]:
        return await self.repository.paginate(self.user.id, page, per_page)

    async def update(self, ident: int, record: RecordUpdate) -> Record:
        obj = await self.get(ident)

        if record.name is not None:
            obj.name = record.name
        if record.username is not None:
            obj.username = AES.encrypt(record.username, cfg.api.secret_encryption)
        if record.password is not None:
            obj.password = AES.encrypt(record.password, cfg.api.secret_encryption)
        if record.url is not None:
            obj.url = record.url

        if record.comment is not None and record.comment.text is not None:
            if obj.comment is None:
                obj.comment = Comment(**record.comment.model_dump())
            else:
                obj.comment.text = record.comment.text

        return await self.repository.update(obj)

    async def delete(self, ident: int) -> Record:
        obj = await self.get(ident)
        await self.repository.delete(obj)
        return obj
