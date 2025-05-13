import logging
from datetime import timedelta

from authx import AuthXConfig
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvConfig(BaseSettings):
    # IP_ADDRESS / PORT
    IP_ADDRESS: str
    PORT: int
    # Connection string config
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    # Session config
    POOL_SIZE: int
    MAX_OVERFLOW: int
    # Uvicorn workers
    UVICORN_WORKERS: int
    # Logging config
    LOG_LEVEL: str
    # Jwt config
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    # Smtp config
    SMTP_LOGIN: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_MAX_POOL: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

class SmtpConfig(BaseSettings):
    login: str
    password: str
    host: str
    port: int
    pool_size: int

class DatabaseConfig(BaseSettings):
    # Connection string config
    username: str
    password: str
    host: str
    port: int
    name: str

    # Session config
    pool_size: int
    max_overflow: int

    # Echo config
    echo: bool
    echo_pool: bool

    # Naming convention
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"

class ApiVersion(BaseSettings):
    root: str # root prefix - /v1/api/...
    recovery: str

class PrefixConfig(BaseSettings):
    v1: ApiVersion

class LoggingConfig(BaseSettings):
    level: str

    @property
    def level_value(self) -> int:
        return logging.getLevelNamesMapping().get(self.level.upper(), logging.DEBUG)

class Settings(BaseSettings):
    db: DatabaseConfig
    jwt: AuthXConfig
    api: PrefixConfig
    log: LoggingConfig
    smtp: SmtpConfig

env_settings = EnvConfig()

settings = Settings(
    db=DatabaseConfig(
        username=env_settings.DB_USERNAME,
        password=env_settings.DB_PASSWORD,
        host=env_settings.DB_HOST,
        port=env_settings.DB_PORT,
        name=env_settings.DB_NAME,
        pool_size=env_settings.POOL_SIZE,
        max_overflow=env_settings.MAX_OVERFLOW,
        echo=False,
        echo_pool=False,
    ),
    jwt=AuthXConfig(
        JWT_ALGORITHM="RS256",
        JWT_TOKEN_LOCATION=["headers"],
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=15),
        JWT_PUBLIC_KEY=env_settings.JWT_PUBLIC_KEY,
        JWT_PRIVATE_KEY=env_settings.JWT_PRIVATE_KEY,
    ),
    api=PrefixConfig(
        v1=ApiVersion(
            root="/v1/api/auth",
            recovery="/v1/api/auth/recovery",
        ),
    ),
    log=LoggingConfig(
        level=env_settings.LOG_LEVEL,
    ),
    smtp=SmtpConfig(
        login=env_settings.SMTP_LOGIN,
        password=env_settings.SMTP_PASSWORD,
        host=env_settings.SMTP_HOST,
        port=env_settings.SMTP_PORT,
        pool_size=env_settings.SMTP_MAX_POOL,
    ),
)
