from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.engine import async_session_factory

from .repositories import CommentRepo, RecordRepo, UserRepo


class Database:
    session: AsyncSession
    user: UserRepo
    record: RecordRepo
    comment: CommentRepo

    def __init__(
        self,
        session: AsyncSession,
        user: UserRepo | None = None,
        record: RecordRepo | None = None,
        comment: CommentRepo | None = None,
    ):
        self.session = session
        self.user = user or UserRepo(session=session)
        self.record = record or RecordRepo(session=session)
        self.comment = comment or CommentRepo(session=session)


async def get_database(
    session: AsyncSession = Depends(async_session_factory),
) -> Database:
    return Database(session=session)
