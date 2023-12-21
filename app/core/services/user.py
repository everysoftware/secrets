from app.core.repositories import UserRepository


class UserService:
    repo: UserRepository

    def __init__(self, repository: UserRepository):
        self.repository = repository
