from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import DatabaseConfig, settings


class DatabaseHelper:
    def __init__(
            self,
            config: DatabaseConfig,
    ) -> None:

        self.engine: AsyncEngine = create_async_engine(
            url=config.async_url,
            echo=False,
            echo_pool=False,
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
        )

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


    async def dispose(self) -> None:
        await self.engine.dispose()

    async def get_async_session(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    config=settings.db,
)
