from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from src.core.config import settings
from src.dependencies.auth import get_user_id_by_access_token
from src.dependencies.service import get_url_service
from src.schemas.url import NewUrlPair, SuccessCreateUrlPair
from src.services.url import UrlService

router = APIRouter(
    prefix=settings.api.v1.url_manager,
    tags=["URL manager"],
)

@router.get("/code={code}")
async def redirect_url(
        code: str,
        service: Annotated[UrlService, Depends(get_url_service)],
) -> RedirectResponse:
    return RedirectResponse(
        status_code=301,
        url=await service.get_real_url(code),
    )

@router.post("/create")
async def create_url_pair(
        creds: NewUrlPair,
        service: Annotated[UrlService, Depends(get_url_service)],
        user_id: Annotated[int, Depends(get_user_id_by_access_token)],
) -> SuccessCreateUrlPair:
    return await service.create_new_url_pair(creds, user_id)
