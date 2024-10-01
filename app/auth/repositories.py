from app.auth.models import UserOrm
from app.auth.schemas import SUserRead
from app.db.repository import AlchemyRepository


class UserRepository(AlchemyRepository[UserOrm, SUserRead]):
    model_type = UserOrm
    schema_type = SUserRead
