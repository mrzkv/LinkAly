import logging
from datetime import timedelta

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class SmtpConfig(BaseSettings):
    login: str
    password: str
    host: str
    port: int
    pool_size: int

    model_config = SettingsConfigDict(
        env_prefix="SMTP_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",

    )

class DatabaseConfig(BaseSettings):
    # Connection string config
    host: str
    username: str
    password: str
    name: str
    port: int

    # Session config
    pool_size: int
    max_overflow: int

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        case_sensitive=False,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"

class ApiVersion(BaseSettings):
    root: str # root prefix - /v1/api/...
    recovery: str

    model_config = SettingsConfigDict(
        env_prefix="PATH_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

class PrefixConfig(BaseSettings):
    v1: ApiVersion

class JWTConfig(BaseSettings):
    access_token_expires: int
    refresh_token_expires: int
    confirm_token_expires: int
    public_key: str
    private_key: str
    issuer: str

    model_config = SettingsConfigDict(
        env_prefix="JWT_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class LoggingConfig(BaseSettings):
    level: str

    @property
    def level_value(self) -> int:
        return logging.getLevelNamesMapping().get(self.level.upper(), logging.DEBUG)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="LOGGING_",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

class CorsConfig(BaseSettings):
    origins: list[str]
    methods: list[str]
    headers: list[str]
    credentials: list[str]

class ServerConfig(BaseSettings):
    host: str
    port: int
    uvicorn_workers: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SERVER_",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

class Settings(BaseSettings):
    server: ServerConfig
    db: DatabaseConfig
    jwt: JWTConfig
    api: PrefixConfig
    log: LoggingConfig
    smtp: SmtpConfig
    cors: CorsConfig


settings = Settings(
    server=ServerConfig(),
    db=DatabaseConfig(),
    jwt=JWTConfig(),
    api=PrefixConfig(
        v1=ApiVersion()
    ),
    log=LoggingConfig(),
    smtp=SmtpConfig(),
    cors=CorsConfig(
        origins=["*"],
        methods=["*"],
        headers=["*"],
        credentials=["*"],
    ),
)
