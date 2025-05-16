from datetime import timedelta

from authx import AuthX, RequestToken, TokenPayload
from authx.schema import (
    CSRFError,
    JWTDecodeError,
    TokenTypeError,
)

from src.core.config import settings


class AuthJWT:
    def __init__(self, jwt: AuthX = AuthX(config=settings.jwt)) -> None:
        self.jwt = jwt

    async def create_access_token(self, user_id: str) -> str:
        return self.jwt.create_access_token(uid=user_id)

    async def create_refresh_token(self, user_id: str) -> str:
        return self.jwt.create_refresh_token(uid=user_id)

    async def create_confirm_token(
            self,
            user_id: str,
            email: str,
            confirm_type: str,
    ) -> str:
        return self.jwt._create_token(
            uid=user_id,
            expiry=timedelta(minutes=20),
            type="confirm",
            data={
                "email": email,
                "confirm_type": confirm_type,
            },
        )

    async def verify_token(
            self,
            token: RequestToken,
            verify_type: bool = True,
    ) -> TokenPayload:
        try:
            return self.jwt.verify_token(token, verify_type)

        except JWTDecodeError as e:
            raise ValueError(e)

        except TokenTypeError as e:
            raise ValueError(e)

        except CSRFError as e:
            raise ValueError(e)


