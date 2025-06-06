from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.config import settings
from src.dependencies.service import get_recovery_service
from src.dependencies.token import get_access_token
from src.schemas.recovery import (
    EmailSetRequest,
    EmailSetResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    NewEmailResponse,
    NewPasswordResponse,
    PasswordChangeRequest,
    PasswordSetRequest,
)
from src.security.jwt import TokenPayload
from src.services import RecoveryService

router = APIRouter(
    prefix=settings.api.v1.recovery,
    tags=["Recovery manager"],
)

@router.post(
    path="/set-email",
    description="Send mail with confirm url.",
)
async def set_email(
        creds: EmailSetRequest,
        access_token: Annotated[
            TokenPayload,
            Depends(get_access_token),
        ],
        service: Annotated[
            RecoveryService,
            Depends(get_recovery_service),
        ],
) -> EmailSetResponse:
    return await service.send_verification_mail(creds, access_token)

@router.get(
    path="/set-email/{code}",
    description="Verify confirm url and set email to user account.",
)
async def confirm_email(
        code: Annotated[
            str,
            "Code from verification mail",
        ],
        service: Annotated[
            RecoveryService,
            Depends(get_recovery_service),
        ],
) -> NewEmailResponse:
    return await service.set_email(code)


@router.post(
    path="/change-password",
    description="To change you need know your old password.",
)
async def change_password(
        creds: PasswordChangeRequest,
        access_token: Annotated[
            TokenPayload,
            Depends(get_access_token),
        ],
        service: Annotated[
            RecoveryService,
            Depends(get_recovery_service),
        ],
) -> NewPasswordResponse:
    return await service.change_password(creds, access_token)


@router.post(
    path="/forgot-password",
    description="Send mail with verification url.",
)
async def forgot_password(
        creds: ForgotPasswordRequest,
        service: Annotated[
            RecoveryService,
            Depends(get_recovery_service),
        ],
) -> ForgotPasswordResponse:
    return await service.send_password_change_mail(creds)

@router.post(
    path="/forgot-password/{code}",
    description="To change you need set your email address before.",
)
async def confirm_password(
        creds: PasswordSetRequest,
        code: Annotated[
            str,
            "Code from email",
        ],
        service: Annotated[
            RecoveryService,
            Depends(get_recovery_service),
        ],
) -> NewPasswordResponse:
    return await service.change_forgotten_password(creds, code)
