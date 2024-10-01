from app.auth.schemas import SUserRead
from app.db.schemas import PageParams
from app.passwords.encryption import encrypt_password, decrypt_password
from app.passwords.schemas import (
    SPasswordCreate,
    SPasswordRead,
    SPasswordPage,
    SPasswordUpdate,
    SPasswordItem,
)
from app.service import Service


class PasswordService(Service):
    async def create(
        self, user: SUserRead, creation: SPasswordCreate
    ) -> SPasswordRead:
        data = encrypt_password(creation.model_dump())
        password = await self.uow.passwords.create(**data, user_id=user.id)
        return SPasswordRead.model_validate(
            decrypt_password(password.model_dump())
        )

    async def get(self, ident: int) -> SPasswordRead | None:
        password = await self.uow.passwords.get(ident)
        if password is None:
            return None
        return SPasswordRead.model_validate(
            decrypt_password(password.model_dump())
        )

    async def get_one(self, ident: int) -> SPasswordRead:
        password = await self.get(ident)
        if password is None:
            raise ValueError("Password not found")
        return password

    async def update(
        self, password: SPasswordRead, update: SPasswordUpdate
    ) -> SPasswordRead:
        data = encrypt_password(update.model_dump(exclude_unset=True))
        password_db = await self.uow.passwords.update(password.id, **data)
        return SPasswordRead.model_validate(
            decrypt_password(password_db.model_dump())
        )

    async def delete(self, password: SPasswordRead) -> SPasswordRead:
        password_db = await self.uow.passwords.delete(password.id)
        return SPasswordRead.model_validate(
            decrypt_password(password_db.model_dump())
        )

    async def search(
        self, user: SUserRead, params: PageParams, query: str | None = None
    ) -> SPasswordPage:
        page = await self.uow.passwords.search(user.id, params, query=query)
        items = [
            SPasswordItem.model_validate(decrypt_password(i.model_dump()))
            for i in page.items
        ]
        return SPasswordPage(items=items)
