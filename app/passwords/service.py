from app.auth.schemas import SUser
from app.core.uow import UOW
from app.core.service import Service
from app.passwords.encryption import PasswordEncryption
from app.passwords.models import PasswordOrm
from app.passwords.schemas import (
    SPasswordCreate,
    SPassword,
    SPasswordEncrypted,
    SPasswordPage,
    SPasswordUpdate,
)
from app.schemas import PageParams


class PasswordService(Service):
    user: SUser

    def __init__(self, uow: UOW, user: SUser):
        self.user = user
        super().__init__(uow)

    async def create(self, creation: SPasswordCreate) -> SPassword:
        encrypted = PasswordEncryption.encrypt_password_create(creation)
        password = PasswordOrm(**encrypted.model_dump())
        password.user_id = self.user.id
        self.uow.passwords.add(password)
        await self.uow.commit()

        return await self.get_one(password.id)

    async def get(self, ident: int) -> SPassword | None:
        model = await self.uow.passwords.get(ident)

        if model is None:
            return None

        scheme = SPasswordEncrypted.model_validate(model)
        decrypted = PasswordEncryption.decrypt_password(scheme)

        return decrypted

    async def get_one(self, ident: int) -> SPassword:
        decrypted = await self.get(ident)

        if decrypted is None:
            raise ValueError("Password not found")

        return decrypted

    async def search(
        self, params: PageParams, query: str | None = None
    ) -> SPasswordPage:
        where = [PasswordOrm.user_id == self.user.id]

        if query:
            where.append(PasswordOrm.title.ilike(f"%{query}%"))

        items = await self.uow.passwords.get_many(
            where=where,
            order_by=[PasswordOrm.updated_at.desc()],
            limit=params.limit,
            offset=params.offset,
        )
        encrypted = [SPasswordEncrypted.model_validate(i) for i in items]
        decrypted = [PasswordEncryption.decrypt_password(i) for i in encrypted]

        return SPasswordPage(items=decrypted)

    async def update(
        self, password_id: int, update: SPasswordUpdate
    ) -> SPassword:
        password = await self.uow.passwords.get(password_id)

        encrypted = PasswordEncryption.encrypt_password_update(update)
        for name, value in encrypted.model_dump(exclude_unset=True).items():
            setattr(password, name, value)

        await self.uow.passwords.update(password)
        await self.uow.commit()

        return await self.get_one(password.id)

    async def delete(self, scheme: SPassword) -> None:
        password = await self.uow.passwords.get(scheme.id)
        await self.uow.passwords.delete(password)
        await self.uow.commit()
