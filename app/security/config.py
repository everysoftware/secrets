from app.schemas import SettingsBase


class SecuritySettings(SettingsBase):
    encryption_secret: str = "changethis"
