from typing import Annotated

from aiosmtplib import SMTP
from authx import RequestToken
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.db_helper import db_helper
from src.core.smtp_helper import smtp_helper
from src.dependencies.token_depends import get_access_token
from src.schemas.recovery import (
    EmailSetRequest,
    EmailSetResponse,
    NewEmailResponse,
)
from src.services.recovery_service import RecoveryService

router = APIRouter(
    prefix=settings.api.v1.recovery,
    tags=["Recovery manager"],
)

async def get_service(
        db_session: Annotated[AsyncSession, Depends(db_helper.get_async_session)],
        smtp_connection: Annotated[SMTP, Depends(smtp_helper.get_smtp_client)],
) -> RecoveryService:
    return RecoveryService(
        db_session=db_session,
        smtp_conn=smtp_connection,
    )

@router.post("/set-email")
async def set_email(
        creds: EmailSetRequest,
        access_token: Annotated[RequestToken, Depends(get_access_token)],
        service: Annotated[RecoveryService, Depends(get_service)],
) -> EmailSetResponse:
    return await service.send_mail(creds, access_token)

@router.get("/set-email/{code}")
async def confirm_email(
        code: Annotated[str, "Code from verification mail"],
        service: Annotated[RecoveryService, Depends(get_service)],
) -> NewEmailResponse:
    return await service.set_email(code)

# @router.post("/forgot-password")
# async def forgot_password(
#         creds: ...,
# ) -> ForgotPasswordResponse:
#     ...
#
# @router.post("/forgot-password/{code}")
# async def confirm_password(
#         creds: PasswordChangeRequest,
#         code: Annotated[str, "Code from email"],
# ) -> NewPasswordResponse:
#     ...
#
# @router.post("/change-password")
# async def change_password(
#         creds: PasswordChangeRequest,
#         access_token: Annotated[RequestToken, Depends(get_access_token)],
# ) -> NewPasswordResponse:
#     ...
