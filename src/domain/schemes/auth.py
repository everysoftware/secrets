from pydantic import Field

from .base import SBase


class SEnableTwoFactor(SBase):
    otp: str = Field(min_length=6, max_length=6, examples=["123456"])


class SQRCode(SBase):
    qr_code: str = Field(examples=["data:image/png;base64, ..."])
