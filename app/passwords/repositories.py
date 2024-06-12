from app.database.repositories import SARepository
from app.passwords.models import PasswordOrm


class PasswordRepository(SARepository[PasswordOrm]):
    model_type = PasswordOrm
