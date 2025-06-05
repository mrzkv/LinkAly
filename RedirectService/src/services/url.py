from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.url import UrlDAO
from src.schemas.url import (
    NewUrlPair,
    SerializedUrlPair,
    SuccessCreateUrlPair,
    UserUrlPair,
)


class UrlService:
    def __init__(
            self,
            session: AsyncSession,
    ) -> None:
        self.urldao = UrlDAO(session)

    async def get_real_url(self, short_url: str) -> str:
        db_urls = await self.urldao.get(short_url=short_url)
        if not db_urls:
            raise HTTPException(status_code=404)
        return db_urls.real_url

    async def create_new_url_pair(
            self,
            data: NewUrlPair,
            creator_id: int,
    ) -> SuccessCreateUrlPair:
        db_urls = await self.urldao.get(short_url=data.short_url)
        if db_urls:
            raise HTTPException(status_code=409, detail="Short url already exists")
        url_pair = await self.urldao.add(
            SerializedUrlPair(
                short_url=data.short_url,
                real_url=data.real_url,
                creator_id=creator_id,
            ),
        )
        return SuccessCreateUrlPair(
            short_url=data.short_url,
            real_url=data.real_url,
            creator_id=url_pair.creator_id,
            url_id=url_pair.id,
        )

    async def get_user_urls(
            self,
            user_id: int,
    ) -> list[UserUrlPair]:
        return [
            UserUrlPair(
                id=url_pair.id,
                short_url=url_pair.short_url,
                real_url=url_pair.real_url,
            ) for url_pair in
            await self.urldao.get(user_id=user_id)
        ]
