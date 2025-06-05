from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from src.core.config import settings
from src.dependencies.auth import get_user_id_by_access_token
from src.dependencies.service import get_url_service
from src.schemas.url import (
    NewUrlPair,
    SuccessCreateUrlPair,
    UserUrlPair,
)
from src.services.url import UrlService

router = APIRouter(
    prefix=settings.api.v1.url_manager,
    tags=["URL manager"],
)

@router.get(
    path="/code={code}",
    name="Redirect user by code",
    description="Use short_url code users redirects to real url",
)
async def redirect_url(
        code: str,
        service: Annotated[UrlService, Depends(get_url_service)],
) -> RedirectResponse:
    return RedirectResponse(
        status_code=301,
        url=await service.get_real_url(code),
    )

@router.post(
    path="/create",
    name="Creates new url pair",
    description="Create new pair: short_url(code) -> real_url",
)
async def create_url_pair(
        creds: NewUrlPair,
        service: Annotated[UrlService, Depends(get_url_service)],
        user_id: Annotated[int, Depends(get_user_id_by_access_token)],
) -> SuccessCreateUrlPair:
    return await service.create_new_url_pair(creds, user_id)

@router.get(
    path="/list",
    name="Returns a list of the users own URLs",
    description="Get list of users own URLs by user id",
)
async def get_list_url(
        user_id: Annotated[int, Depends(get_user_id_by_access_token)],
        service: Annotated[UrlService, Depends(get_url_service)],
) -> list[UserUrlPair]:
    return await service.get_user_urls(user_id)

