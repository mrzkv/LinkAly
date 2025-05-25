from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_helper import db_helper
from src.services.url import UrlService


async def get_url_service(
        session: AsyncSession = Depends(db_helper.get_async_session),
) -> UrlService:
    return UrlService(session)
