from typing import AsyncGenerator, Optional

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, IntegerIDMixin, exceptions, models,
                           schemas)

from app.core.config import cfg
from app.core.models import User
from app.core.repositories import get_user_db
from app.tasks import send_email
from .email import thank_you
from ..utils import SHA256


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = cfg.api.secret_auth
    verification_token_secret = cfg.api.secret_auth

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        # Added master password hashing
        master_password = user_dict.pop("master_password")
        user_dict["hashed_master"] = SHA256.hash_with_salt(master_password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def on_after_register(self, user: User, request: Request | None = None):
        print(f"User {user.id} has registered.")

        send_email.delay(thank_you(user))


async def get_user_manager(
        user_db=Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)
