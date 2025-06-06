from typing import Annotated

import jwt
from fastapi import Header, HTTPException

from src.core.config import security
from src.core.logging_promtail import logger


async def get_user_id_by_access_token(
        access_token: Annotated[
            str | None,
            Header(alias="x-access-token"),
        ],
) -> int:
    if not access_token:
        raise HTTPException(status_code=401)
    try:
        token_payload = jwt.decode(
            access_token,
            security.public_key,
            algorithms=["RS256"],
        )
    except jwt.ExpiredSignatureError as e:
        logger.debug(f"Expired token: {access_token}")
        raise HTTPException(status_code=401) from e
    except jwt.InvalidTokenError as e:
        logger.info(f"Invalid token: {access_token}, {e}")
        raise HTTPException(status_code=401) from e

    try:
        return int(token_payload["sub"])
    except KeyError as e:
        logger.warning(f"KeyError, Invalid access token: {access_token}")
        raise HTTPException(status_code=401) from e
    except TypeError as e:
        logger.warning(f"TypeError, Invalid access token: {access_token}")
        raise HTTPException(status_code=401) from e
