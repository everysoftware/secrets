from src.application.auth import (
    generate_uri,
    generate_secret,
    generate_qr_code,
)
from src.domain.schemes import SQRCode
from src.domain.schemes import SUser
from .base import Service


class AuthService(Service):
    async def _reset_otp_secret(self, user: SUser) -> SUser:
        """Update user's OTP secret."""
        async with self.uow:
            model = await self.uow.users.get(user.id)
            model.otp_secret = generate_secret()
            await self.uow.users.update(model)

            return SUser.model_validate(model)

    async def connect_two_factor(self, user: SUser) -> SQRCode:
        """Connect user to authenticator app."""
        user = await self._reset_otp_secret(user)

        if user.otp_secret is None:
            raise ValueError("OTP secret is not set.")

        uri = generate_uri(user.otp_secret, user.email)
        qr_code = generate_qr_code(uri)

        return SQRCode(qr_code=f"data:image/png;base64,{qr_code}")

    async def enable_two_factor(self, user: SUser) -> SUser:
        """Enable 2FA for user."""
        async with self.uow:
            model = await self.uow.users.get(user.id)
            model.two_factor = True
            await self.uow.users.update(model)

            return SUser.model_validate(model)
