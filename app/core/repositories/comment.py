from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Comment
from .base import Repository


class CommentRepo(Repository[Comment]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Comment, session=session)
