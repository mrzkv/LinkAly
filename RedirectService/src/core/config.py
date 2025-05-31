import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.logging_promtail import logger
from src.utils.public_key_reciever import get_public_key


class ServerConfig(BaseSettings):
    host: str
    port: int
    workers: int
    public_key_distributor_url: str
    default_public_key: str

    model_config = SettingsConfigDict(
        env_prefix="SERVER_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

class DatabaseConfig(BaseSettings):
    user: str
    password: str
    db: str # Database name
    host: str
    port: int

    pool_size: int
    max_overflow: int

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

class LoggingConfig(BaseSettings):
    level: str

    model_config = SettingsConfigDict(
        env_prefix="LOGGING_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def level_value(self) -> int:
        return logging.getLevelNamesMapping().get(self.level.upper(), logging.DEBUG)

class CorsConfig(BaseSettings):
    origins: list[str]
    methods: list[str]
    headers: list[str]
    credentials: list[str]

class MiddlewareConfig(BaseSettings):
    cors: CorsConfig

class ApiVersionConfig(BaseSettings):
    root: str
    url_manager: str

class PrefixConfig(BaseSettings):
    v1: ApiVersionConfig

class JWTConfig(BaseSettings):
    public_key: str

class Settings(BaseSettings):
    server: ServerConfig
    db: DatabaseConfig
    api: PrefixConfig
    log: LoggingConfig
    middleware: MiddlewareConfig

settings = Settings(
    server=ServerConfig(),
    db=DatabaseConfig(),
    api=PrefixConfig(
        v1=ApiVersionConfig(
            root="/v1/api/redirect",
            url_manager="/v1/api/redirect/manager",
        ),
    ),
    log=LoggingConfig(),
    middleware=MiddlewareConfig(
        cors=CorsConfig(
            origins=["*"],
            methods=["*"],
            headers=["*"],
            credentials=["*"],
        ),
    ),
)

try:
    public_key = get_public_key()
except Exception:
    logger.warning("Public key not found, using default values")
    public_key = settings.server.default_public_key

security = JWTConfig(
    public_key=public_key,
)
