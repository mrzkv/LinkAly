from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import AbstractDAO
from src.schemas.url import SerializedUrlPair
from src.tables.urlpair import UrlPair


class UrlDAO(AbstractDAO):
    def __init__(
            self,
            session: AsyncSession,
    ) -> None:
        self.session = session

    async def get(
            self,
            **kwargs: dict,
    ) -> UrlPair | None:
        """
        This function takes positional arguments
        and executes the query with them.

        >>> id = 1
        'SELECT * FROM url_pairs WHERE id = 1'
        >>> short_url = mrzkv
        'SELECT * FROM url_pairs WHERE short_url = mrzkv'
        >>> real_url = mrzkv.example.com
        'SELECT * FROM url_pairs WHERE real_url = mrzkv.example.com'
        """
        if len(kwargs.keys()) != 1:
            raise ValueError("Only 1 positional argument is allowed")

        column, value = next(iter(kwargs.items()))
        allowed_columns = {"short_url", "real_url", "id"}

        if column not in allowed_columns:
            raise ValueError("Invalid column")

        result = await self.session.execute(
            select(UrlPair)
            .where(getattr(UrlPair, column) == value),
        )
        return result.scalars().first()

    async def add(
            self,
            data: SerializedUrlPair,
    ) -> UrlPair | None:
        result = await self.session.execute(
            insert(UrlPair)
            .values(
                short_url=data.short_url,
                real_url=data.real_url,
                creator_id=data.creator_id,
            )
            .returning(UrlPair),
        )
        await self.session.commit()
        return result.scalars().first()

    async def delete(
            self,
            url_id: int,
    ) -> UrlPair | None:
        result = await self.session.execute(
            delete(UrlPair)
            .where(UrlPair.id == url_id)
            .returning(UrlPair),
        )
        await self.session.commit()
        return result.scalars().first()

    async def change_real_url(
            self,
            url_id: int,
            real_url: str,
    ) -> UrlPair | None:
        result = await self.session.execute(
            update(UrlPair)
            .where(UrlPair.id == url_id)
            .values(real_url=real_url)
            .returning(UrlPair),
        )
        await self.session.commit()
        return result.scalars().first()

    async def change_short_url(
            self,
            url_id: int,
            short_url: str,
    ) -> UrlPair | None:
        result = await self.session.execute(
            update(UrlPair)
            .where(UrlPair.id == url_id)
            .values(short_url=short_url)
            .returning(UrlPair),
        )
        await self.session.commit()
        return result.scalars().first()
