from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from .base import SQLAlchemyRepository
from ..models import Comment, Record


class RecordRepository(SQLAlchemyRepository[Record]):
    model = Record

    async def create(self, record: Record, comment: Comment) -> Record:
        if comment is not None:
            self.session.add(comment)
            record.comment = comment

        self.new(record)
        await self.session.commit()

        return record

    async def count(self, user_id: int) -> int:
        stmt = select(func.count(Record.id)).where(Record.user_id == user_id)
        res = await self.session.execute(stmt)
        count = res.scalar_one()

        return count

    async def paginate(
            self, user_id: int, page: int, per_page: int
    ) -> Sequence[Record]:
        stmt = (
            select(Record)
            .where(Record.user_id == user_id)
            .order_by(Record.name)
            .options(joinedload(Record.comment))  # noqa E501
        )
        offset = (page - 1) * per_page
        stmt = stmt.limit(per_page).offset(offset)
        result = await self.session.execute(stmt)
        records = result.scalars().all()

        return records

    async def update(self, record: Record) -> Record:
        obj = await self.merge(record)
        await self.session.commit()
        return obj

    async def delete(self, record: Record) -> None:
        await self.session.delete(record)
        await self.session.commit()
