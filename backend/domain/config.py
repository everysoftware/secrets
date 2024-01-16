import enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, enum.Enum):
    LOCAL = "local"
    TESTING = "testing"
    PRODUCTION = "production"

    @property
    def is_debug(self) -> bool:
        return self in (self.LOCAL, self.TESTING)

    @property
    def is_testing(self) -> bool:
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        return self == self.PRODUCTION


class DomainSettings(BaseSettings):
    environment: Environment
    product_name: str

    model_config = SettingsConfigDict(env_prefix="domain_")


domain_settings = DomainSettings()
