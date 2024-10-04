from app.schemas import SettingsBase


class PasswordSettings(SettingsBase):
    encryption_secret: str = "changethis"
