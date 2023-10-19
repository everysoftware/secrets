from sqlalchemy.ext.asyncio import AsyncSession

from .repo import Repository
from ..models import Comment


class CommentRepo(Repository[Comment]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Comment, session=session)

    def new(
            self,
            text: str,
    ) -> Comment:
        new_comment = Comment(
            text=text,
        )
        self.session.add(new_comment)
        return new_comment
