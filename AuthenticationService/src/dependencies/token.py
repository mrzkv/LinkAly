from typing import Annotated

from fastapi import Header, HTTPException

from src.core.logging_promtail import logger
from src.security.jwt import TokenPayload, auth_jwt


async def get_access_token(
        x_access_token: Annotated[
            str | None,
            Header(alias="x-access-token"),
        ],
) -> TokenPayload:
    if not x_access_token:
        raise HTTPException(status_code=401,
                            detail="Access token is required")
    try:
        return auth_jwt.verify_token(x_access_token)
    except ValueError as e:
        logger.info(e)
        raise HTTPException(status_code=401)

async def get_refresh_token(
        x_refresh_token: Annotated[
            str | None,
            Header(alias="x-refresh-token"),
        ],
) -> TokenPayload:
    if not x_refresh_token:
        raise HTTPException(status_code=401,
                            detail="Refresh token is required")
    try:
        return auth_jwt.verify_token(x_refresh_token)
    except ValueError as e:
        logger.info(e)
        raise HTTPException(status_code=401)
