from authx import AuthX, TokenPayload
from authx.exceptions import FreshTokenRequiredError
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

    async def verify_token(self, token: str) -> TokenPayload:
        try:
            return self.jwt.verify_token(token)

        except JWTDecodeError as e:
            raise ValueError(e)

        except TokenTypeError as e:
            raise ValueError(e)

        except FreshTokenRequiredError as e:
            raise ValueError(e)

        except CSRFError as e:
            raise ValueError(e)
