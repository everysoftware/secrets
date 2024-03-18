from src.domain.schemes import (
    SPassword,
    SUser,
    SPasswordEncrypted,
    SPasswordCreate,
    SPasswordUpdate,
    SPasswordItem,
    SPage,
    SParams,
)
from src.infrastructure.db import UnitOfWork
from src.infrastructure.models import PasswordOrm
from src.infrastructure.repositories import EntityNotFound
from .base import Service
from .security import SecurityService


class PasswordService(Service):
    security: SecurityService

    def __init__(self, uow: UnitOfWork, security: SecurityService):
        super().__init__(uow)
        self.security = security

    async def create(self, user: SUser, scheme: SPasswordCreate) -> SPassword:
        """Create a new password for the user."""
        encrypted = self.security.encrypt_password_create(scheme)
        model = PasswordOrm(**encrypted.model_dump())
        model.user_id = user.id

        async with self.uow:
            await self.uow.passwords.create(model)

        return await self.get(model.id)

    async def get_or_none(self, ident: int) -> SPassword | None:
        """Get a password by its id. Return `None` if not found."""
        async with self.uow:
            model = await self.uow.passwords.get_or_none(ident)

        if model is None:
            return None

        scheme = SPasswordEncrypted.model_validate(model)
        decrypted = self.security.decrypt_password(scheme)

        return decrypted

    async def get(self, ident: int) -> SPassword:
        """Get a password by its id. Raise `EntityNotFound` if not found."""

        async with self.uow:
            try:
                model = await self.uow.passwords.get(ident)
            except EntityNotFound:
                raise

        scheme = SPasswordEncrypted.model_validate(model)
        decrypted = self.security.decrypt_password(scheme)

        return decrypted

    async def search(
        self, user: SUser, params: SParams, query: str | None = None
    ) -> SPage[SPasswordItem]:
        """Search for passwords by user."""
        where = [PasswordOrm.user_id == user.id]

        if query is not None:
            where.append(PasswordOrm.title.ilike(f"%{query}%"))

        async with self.uow:
            return await self.uow.passwords.search(
                params,
                where=where,
                order_by=[PasswordOrm.title.asc()],
            )

    async def update(
        self, scheme: SPassword, update_scheme: SPasswordUpdate
    ) -> SPassword:
        """Update a password."""
        async with self.uow:
            model = await self.uow.passwords.get(scheme.id)

            encrypted = self.security.encrypt_password_update(update_scheme)
            for name, value in encrypted.model_dump(exclude_unset=True).items():
                setattr(model, name, value)

            await self.uow.passwords.update(model)

        return await self.get(model.id)

    async def delete(self, scheme: SPassword) -> None:
        """Delete a password."""
        async with self.uow:
            model = await self.uow.passwords.get(scheme.id)
            await self.uow.passwords.delete(model)
