from domain.user import BaseUserRepository


class UserService:
    repository: BaseUserRepository

    def __init__(self, repository: BaseUserRepository):
        self.repository = repository
