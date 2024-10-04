from app.schemas import SettingsBase


class AuthSettings(SettingsBase):
    auth_secret: str = "changethis"
    auth_token_lifetime: int = 3600
