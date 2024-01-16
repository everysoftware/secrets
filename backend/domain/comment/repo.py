import abc

from domain.base.repo import BaseRepository
from domain.comment.schemes import CommentRead, CommentCreate, CommentUpdate


class BaseCommentRepository(BaseRepository, abc.ABC):
    read_scheme = CommentRead
    create_scheme = CommentCreate
    update_scheme = CommentUpdate
