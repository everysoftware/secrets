from domain.comment import BaseCommentRepository


class CommentService:
    repository: BaseCommentRepository

    def __init__(self, repo: BaseCommentRepository):
        self.repository = repo
