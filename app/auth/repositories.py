from app.database.repositories import SARepository
from app.auth.models import UserOrm


class UserRepository(SARepository[UserOrm]):
    model = UserOrm
