from typing import Annotated
from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from src.core.config import settings
from src.dependencies.service import get_url_service
from src.services.url import UrlService

router = APIRouter(
    prefix=settings.api.v1.url_manager,
    tags=["URL manager"],
)

@router.get("/{code}")
async def redirect_url(
        code: str,
        service: Annotated[UrlService, Depends(get_url_service)],
) -> RedirectResponse:
    return RedirectResponse(
        status_code=301,
        url=await service.get_real_url(code),
    )

@router.post("/{code}")
async def create_url_pair(
        code: str,
        service: Annotated[UrlService, Depends(get_url_service)],
): pass