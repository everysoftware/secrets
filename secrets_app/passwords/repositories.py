from secrets_app.database.repositories import SARepository
from secrets_app.passwords.models import PasswordOrm


class PasswordRepository(SARepository[PasswordOrm]):
    model_type = PasswordOrm
