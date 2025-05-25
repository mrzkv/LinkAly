from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.url import UrlDAO

from fastapi import HTTPException

class UrlService:
    def __init__(
            self,
            session: AsyncSession,
    ) -> None:
        self.dao = UrlDAO(session)

    async def get_real_url(self, short_url: str) -> str:
        db_urls = await self.dao.get(short_url=short_url)
        if not db_urls:
            raise HTTPException(status_code=404)
        return f"http://{db_urls.real_url}"

