from pydantic_settings import BaseSettings, SettingsConfigDict


class EncryptionSettings(BaseSettings):
    secret: str

    model_config = SettingsConfigDict(env_prefix="encryption_")


class AppSettings(BaseSettings):
    encryption: EncryptionSettings = EncryptionSettings()


app_settings = AppSettings()
