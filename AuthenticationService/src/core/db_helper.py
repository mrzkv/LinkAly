from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __abstract__ = True


class DatabaseHelper:
    def __init__(
            self,
            url: str,
            pool_size: int,
            max_overflow: int,
            *,
            echo: bool = False,
            echo_pool: bool = False,
    ) -> None:

        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
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


