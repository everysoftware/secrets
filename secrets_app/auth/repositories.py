from secrets_app.database.repositories import SARepository
from secrets_app.auth.models import UserOrm


class UserRepository(SARepository[UserOrm]):
    model = UserOrm
