from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class BackendBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SettingsBase(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
