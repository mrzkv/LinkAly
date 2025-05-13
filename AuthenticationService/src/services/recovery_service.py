from email.mime.text import MIMEText

import aiosmtplib
from authx import RequestToken
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import env_settings, settings
from src.core.logging_promtail import logger
from src.repositories.smtp_repository import SMTPRepository
from src.repositories.user_repository import UsersRepository
from src.schemas.recovery import EmailSetRequest, EmailSetResponse, NewEmailResponse
from src.security.jwt import AuthJWT


class RecoveryService:
    def __init__(
            self,
            db_session: AsyncSession,
            smtp_conn: aiosmtplib.SMTP,
            jwt: AuthJWT = AuthJWT(),
    ) -> None:
        self.db_repository = UsersRepository(db_session)
        self.smtp_repository = SMTPRepository(smtp_conn)
        self.jwt = jwt

    async def send_mail(
            self,
            data: EmailSetRequest,
            access_token: RequestToken,
    ) -> EmailSetResponse:
        try:
            token_payload = await self.jwt.verify_token(access_token)
        except ValueError as e:
            logger.info(f"Invalid token: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        if await self.db_repository.get(email=data.email):
            raise HTTPException(status_code=400, detail="Email already set")
        confirm_token = await self.jwt.create_confirm_token(user_id=token_payload.sub,
                                                            email=data.email)
        verify_link = f"http://{env_settings.IP_ADDRESS}:{env_settings.PORT}{settings.api.v1.recovery}/set-email/{confirm_token}"
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
        confirm_token = RequestToken(
            token=confirm_token,
            type="access",
            location="query",
        )
        try:
            token_payload = await self.jwt.verify_token(
                token=confirm_token,
                verify_type=False,
            )
        except ValueError as e:
            logger.info(f"Invalid token: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        if token_payload.type != "confirm":
            raise HTTPException(status_code=401, detail="Invalid token")
        try:
            email=token_payload.email
        except AttributeError as e:
            logger.info(f"Invalid token: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")

        await self.db_repository.set_email(
            email=email,
            user_id=int(token_payload.sub),
        )

        return NewEmailResponse(email=email)
