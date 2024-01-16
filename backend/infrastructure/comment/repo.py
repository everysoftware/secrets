from domain.comment import BaseCommentRepository
from infrastructure.base.repo import SARepository
from .models import Comment


class CommentRepository(BaseCommentRepository, SARepository):
    model = Comment
