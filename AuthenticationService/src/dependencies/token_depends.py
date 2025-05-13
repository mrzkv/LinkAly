from typing import Annotated

from authx import RequestToken
from fastapi import Header, HTTPException

from src.core.config import settings


async def get_access_token(
        x_access_token: Annotated[str | None, Header(alias="x-access-token")],
) -> RequestToken:
    if not x_access_token:
        raise HTTPException(status_code=401,
                            detail="Access token is required")
    return RequestToken(
        token=x_access_token,
        type="access",
        location=settings.jwt.JWT_TOKEN_LOCATION[0],
    )

async def get_refresh_token(
        x_refresh_token: Annotated[str | None, Header(alias="x-refresh-token")],
) -> RequestToken:
    if not x_refresh_token:
        raise HTTPException(status_code=401,
                            detail="Refresh token is required")
    return RequestToken(
        token=x_refresh_token,
        type="refresh",
        location=settings.jwt.JWT_TOKEN_LOCATION[0],
    )
