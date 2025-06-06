from datetime import UTC, datetime, timedelta

import jwt
from pydantic import BaseModel

from src.core.config import JWTConfig, settings


class TokenPayload(BaseModel):
    sub: str
    typ: str
    iat: datetime
    exp: datetime
    iss: str
    email: str | None = None
    confirm_type: str | None = None


class AuthJWT:
    def __init__(self, config: JWTConfig) -> None:
        self.private_key = config.private_key
        self.public_key = config.public_key
        self.access_exp = timedelta(config.access_token_expires)
        self.refresh_exp = timedelta(config.refresh_token_expires)
        self.confirm_exp = timedelta(config.confirm_token_expires)
        self.issuer = config.issuer

    def create_token_payload(
            self,
            subject: str,  # user_id
            token_type: str, # ['access', 'refresh', 'confirm']
            expires_at: datetime, # expiry time
            email: str | None = None, # for confirm token
            confirm_type: str | None = None, # ['verify_mail', 'password_change']
    ) -> TokenPayload:
        if not isinstance(subject, str):
            raise TypeError("subject must be a string")

        issued_at = datetime.now(UTC)

        return TokenPayload(
            sub=subject,
            typ=token_type,
            iat=issued_at,
            exp=expires_at,
            iss=self.issuer,
            email=email,
            confirm_type=confirm_type,
        )

    def create_access_token(self, user_id: str) -> str:
        payload = self.create_token_payload(
            subject=user_id,
            token_type="access",
            expires_at=datetime.now(UTC) + self.access_exp,
        )
        return jwt.encode(
            payload=payload.model_dump(exclude_none=True),
            algorithm="RS256",
            key=self.private_key,
        )

    def create_refresh_token(self, user_id: str) -> str:
        payload = self.create_token_payload(
            subject=user_id,
            token_type="refresh",
            expires_at=datetime.now(UTC) + self.refresh_exp,
        )
        return jwt.encode(
            payload=payload.model_dump(exclude_none=True),
            algorithm="RS256",
            key=self.private_key,
        )

    def create_confirm_token(
            self,
            confirm_type: str,
            user_id: str,
            email: str,
    ) -> str:
        payload = self.create_token_payload(
            subject=user_id,
            token_type="confirm",
            expires_at=datetime.now(UTC) + self.confirm_exp,
            email=email,
            confirm_type=confirm_type,
        )
        return jwt.encode(
            payload=payload.model_dump(exclude_none=True),
            algorithm="RS256",
            key=self.private_key,
        )

    def verify_token(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(
                jwt=token,
                key=self.public_key,
                algorithms=["RS256"],
                issuer=settings.jwt.issuer,
            )
            if payload["typ"] not in ["access", "refresh", "confirm"]:
                raise ValueError("Invalid token type")

            return TokenPayload(**payload)

        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidSignatureError:
            raise ValueError("Invalid signature")
        except jwt.InvalidTokenError as e:
            msg = f"Invalid token: {e}"
            raise ValueError(msg)

auth_jwt = AuthJWT(settings.jwt)
