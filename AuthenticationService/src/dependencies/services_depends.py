from typing import Annotated

from aiosmtplib import SMTP
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_helper import db_helper
from src.core.smtp_helper import smtp_helper
from src.services import RecoveryService, UserService


async def get_users_service(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.get_async_session),
        ],
) -> UserService:
    return UserService(session)

async def get_recovery_service(
        db_session: Annotated[
            AsyncSession,
            Depends(db_helper.get_async_session),
        ],
        smtp_connection: Annotated[
            SMTP,
            Depends(smtp_helper.get_smtp_client),
        ],
) -> RecoveryService:
    return RecoveryService(
        db_session=db_session,
        smtp_conn=smtp_connection,
    )
