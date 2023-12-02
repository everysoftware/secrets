from sqlalchemy.ext.asyncio import AsyncSession

from .repositories import CommentRepo, CredentialsRepo, RecordRepo, UserRepo


class Database:
    session: AsyncSession
    user: UserRepo
    record: RecordRepo
    comment: CommentRepo
    credentials: CredentialsRepo

    def __init__(
        self,
        session: AsyncSession,
        user: UserRepo | None = None,
        record: RecordRepo | None = None,
        comment: CommentRepo | None = None,
        credentials: CredentialsRepo | None = None,
    ):
        self.session = session
        self.user = user or UserRepo(session=session)
        self.record = record or RecordRepo(session=session)
        self.comment = comment or CommentRepo(session=session)
        self.credentials = credentials or CredentialsRepo(session=session)
