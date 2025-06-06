from email.mime.text import MIMEText

import aiosmtplib
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.logging_promtail import logger
from src.repositories.smtp import SMTPRepository
from src.repositories.user import UsersRepository
from src.schemas.recovery import (
    EmailSetRequest,
    EmailSetResponse,
    ForgotPasswordResponse,
    NewEmailResponse,
    NewPasswordResponse,
    PasswordChangeRequest,
    PasswordSetRequest,
)
from src.security.argon_hasher import ArgonHasher
from src.security.jwt import AuthJWT, TokenPayload


class RecoveryService:
    def __init__(
            self,
            db_session: AsyncSession,
            smtp_conn: aiosmtplib.SMTP,
    ) -> None:
        self.db_repository = UsersRepository(db_session)
        self.smtp_repository = SMTPRepository(smtp_conn)
        self.hasher = ArgonHasher()
        self.jwt = AuthJWT(settings.jwt)

    async def send_verification_mail(
            self,
            data: EmailSetRequest,
            token_payload: TokenPayload,
    ) -> EmailSetResponse:
        db_user = await self.db_repository.get(id=int(token_payload.sub))
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        if db_user.email:
            raise HTTPException(status_code=400, detail="Email already set")
        confirm_token = self.jwt.create_confirm_token(
            user_id=token_payload.sub,
            email=data.email,
            confirm_type="verify_mail",
        )
        verify_link = f"http://{settings.server.host}:{settings.server.port}{settings.api.v1.recovery}/set-email/{confirm_token}"
        body = (f"Hello, its LinkAly verification mail.\n"
                f"Click this link to verify your email.\n"
                f"link: {verify_link}\n")
        message = MIMEText(body, "plain", "utf-8")
        message["From"] = settings.smtp.login
        message["To"] = data.email
        message["Subject"] = "verification email"
        await self.smtp_repository.send(message)
        return EmailSetResponse()

    async def set_email(
            self,
            confirm_token: str,
    ) -> NewEmailResponse:
        try:
            token_payload = self.jwt.verify_token(confirm_token)
        except ValueError:
            logger.info(f"Invalid token: {confirm_token}")
            raise HTTPException(status_code=404)

        if token_payload.typ != "confirm":
            raise HTTPException(status_code=401, detail="Invalid token")
        if token_payload.confirm_type != "verify_mail":
            raise HTTPException(status_code=401, detail="Invalid token")

        await self.db_repository.set_email(
            email=token_payload.email,
            user_id=int(token_payload.sub),
        )
        return NewEmailResponse(email=token_payload.email)

    async def change_password(
            self,
            data: PasswordChangeRequest,
            token_payload: TokenPayload,
    ) -> NewPasswordResponse:
        db_user = await self.db_repository.get(id=int(token_payload.sub))
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        try:
            if not await self.hasher.verify_password(
                    plain_password=str(data.old_password),
                    hashed_password=str(db_user.hashed_password)):
                raise HTTPException(status_code=401, detail="Invalid old password")
        except ValueError:
            raise HTTPException(status_code=401, detail="Old password is invalid")
        new_hashed_password = await self.hasher.hash_password(data.new_password)
        await self.db_repository.set_password(db_user.id, new_hashed_password)
        return NewPasswordResponse()

    async def send_password_change_mail(
            self,
            data: PasswordChangeRequest,
    ) -> ForgotPasswordResponse:
        db_user = await self.db_repository.get(email=str(data.email))
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        confirm_token = await self.jwt.create_confirm_token(
            user_id=str(db_user.id),
            email=data.email,
            confirm_type="password_change",
        )
        verify_link = f"http://{env_settings.IP_ADDRESS}:{env_settings.PORT}{settings.api.v1.recovery}/forgot-password/{confirm_token}"
        body = (f"Hello, its LinkAly verification mail.\n"
                f"Click this link to change your password.\n"
                f"link: {verify_link}\n")
        message = MIMEText(body, "plain", "utf-8")
        message["From"] = settings.smtp.login
        message["To"] = data.email
        message["Subject"] = "verification email"
        await self.smtp_repository.send(message)
        return ForgotPasswordResponse()

    async def change_forgotten_password(
            self,
            data: PasswordSetRequest,
            confirm_token: str,
    ) -> NewPasswordResponse:
        try:
            token_payload = await self.jwt.verify_token(
                token=confirm_token,
                verify_type=False,
            )
        except ValueError as e:
            logger.info(f"Invalid token: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        if token_payload.typ != "confirm":
            raise HTTPException(status_code=401, detail="Invalid token")
        if token_payload.confirm_type != "password_change":
            raise HTTPException(status_code=401, detail="Invalid token")

        hashed_password = await self.hasher.hash_password(data.password)
        await self.db_repository.set_password(
            user_id=int(token_payload.sub),
            hashed_password=hashed_password,
        )
        return NewPasswordResponse()
