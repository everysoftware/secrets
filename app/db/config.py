from app.schemas import SettingsBase


class DBSettings(SettingsBase):
    db_url: str = "postgresql+asyncpg://postgres:changethis@db:5432/app"
    db_echo: bool = False
