import logging

from authx import AuthXConfig
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    # Connection
    username: str
    password: str
    host: str
    port: int
    name: str

    # Session config
    pool_size: int
    max_overflow: int

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def sync_url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

class ApiVersion(BaseSettings):
    root: str # root prefix - /v1/api/...

class PrefixConfig(BaseSettings):
    v1: ApiVersion

class LoggingConfig(BaseSettings):
    level: str

    @property
    def level_value(self) -> int:
        return logging.getLevelNamesMapping().get(self.level.upper(), logging.DEBUG)

class Settings(BaseSettings):
    env: SettingsConfigDict
    db: DatabaseConfig
    jwt: AuthXConfig
    api: PrefixConfig
    log: LoggingConfig
