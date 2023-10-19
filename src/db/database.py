from sqlalchemy.ext.asyncio import AsyncSession

from .repositories import CommentRepo, RecordRepo, UserRepo, AuthDataRepo


class Database:
    session: AsyncSession
    user: UserRepo
    record: RecordRepo
    comment: CommentRepo
    auth_data: AuthDataRepo

    def __init__(
            self,
            session: AsyncSession,
            user: UserRepo = None,
            record: RecordRepo = None,
            comment: CommentRepo = None,
            auth_data: AuthDataRepo = None,
    ):
        self.session = session
        self.user = user or UserRepo(session=session)
        self.record = record or RecordRepo(session=session)
        self.comment = comment or CommentRepo(session=session)
        self.auth_data = auth_data or AuthDataRepo(session=session)
