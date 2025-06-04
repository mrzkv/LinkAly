from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.logging_promtail import logger
from src.repositories.user_repository import UsersRepository
from src.schemas.user import (
    SerializedUser,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserMe,
)
from src.security.argon_hasher import ArgonHasher
from src.security.jwt import AuthJWT, TokenPayload, auth_jwt


class UserService:
    def __init__(
            self,
            session: AsyncSession,
            jwt: AuthJWT = AuthJWT(settings.jwt),
            hasher: ArgonHasher = ArgonHasher(),
    ) -> None:
        self.repository = UsersRepository(session)
        self.jwt = auth_jwt
        self.hasher = hasher

    async def register_user(self, user: UserCreate) -> TokenResponse:
        if await self.repository.get(login=user.login):
            raise HTTPException(status_code=409, detail="Login already exists")
        serialized_user = SerializedUser(
            login=user.login,
            hashed_password=await self.hasher.hash_password(user.password),
        )
        user_id = await self.repository.add(serialized_user)
        return TokenResponse(
            access_token=self.jwt.create_access_token(str(user_id)),
            refresh_token=self.jwt.create_refresh_token(str(user_id)),
            user_id=user_id,
        )

    async def login_user(self, user: UserLogin) -> TokenResponse:
        db_user = await self.repository.get(login=user.login)
        if not db_user:
            raise HTTPException(status_code=401,
                                detail="Incorrect password or login")
        try:
            if not await self.hasher.verify_password(
                    plain_password=user.password,
                    hashed_password=db_user.hashed_password):
                raise HTTPException(status_code=401,
                                    detail="Incorrect password or login")
        except ValueError:
            raise HTTPException(status_code=401,
                                detail="Incorrect password or login")
        return TokenResponse(
            access_token=self.jwt.create_access_token(str(db_user.id)),
            refresh_token=self.jwt.create_refresh_token(str(db_user.id)),
            user_id=db_user.id,
        )

    async def refresh_user_token(self, token_payload: TokenPayload) -> TokenResponse:
        db_user = await self.repository.get(id=int(token_payload.sub))
        if not db_user:
            logger.info(f"Invalid user in token: {token_payload}")
            raise HTTPException(status_code=401, detail="Invalid token")

        return TokenResponse(
            access_token=self.jwt.create_access_token(str(db_user.id)),
            user_id=db_user.id,
        )

    async def get_user_profile(
            self,
            token_payload: TokenPayload,
    ) -> UserMe:
        db_user = await self.repository.get(id=int(token_payload.sub))
        if not db_user:
            logger.error(f"Invalid user in token: {token_payload.sub}")
            raise HTTPException(status_code=401)
        return UserMe(
            id=db_user.id,
            login=db_user.login,
            email=db_user.email,
        )
