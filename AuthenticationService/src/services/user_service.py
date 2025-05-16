from authx import RequestToken
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logging_promtail import logger
from src.repositories.user_repository import UsersRepository
from src.schemas.user import SerializedUser, TokenResponse, UserCreate, UserLogin
from src.security.argon_hasher import ArgonHasher
from src.security.jwt import AuthJWT


class UserService:
    def __init__(
            self,
            session: AsyncSession,
            jwt: AuthJWT = AuthJWT(),
            hasher: ArgonHasher = ArgonHasher(),
    ) -> None:
        self.repository = UsersRepository(session)
        self.jwt = jwt
        self.hasher = hasher

    async def register_user(self, user: UserCreate) -> TokenResponse:
        if await self.repository.get(login=user.login):
            raise HTTPException(status_code=409, detail="Login already exists")
        serialized_user = SerializedUser(
            login=user.login,
            hashed_password=await self.hasher.hash_password(user.password),
        )
        user_id = await self.repository.add(serialized_user)
        access_token = await self.jwt.create_access_token(str(user_id))
        refresh_token = await self.jwt.create_refresh_token(str(user_id))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user_id,
        )

    async def login_user(self, user: UserLogin) -> TokenResponse:
        db_user = await self.repository.get(login=user.login)
        if not db_user:
            raise HTTPException(status_code=401,
                                detail="Incorrect password or login")
        try:
            if not await self.hasher.verify_password(plain_password=user.password,
                                                     hashed_password=db_user.hashed_password):
                raise HTTPException(status_code=401,
                                    detail="Incorrect password or login")
        except ValueError:
            raise HTTPException(status_code=401,
                                detail="Incorrect password or login")
        access_token = await self.jwt.create_access_token(str(db_user.id))
        refresh_token = await self.jwt.create_refresh_token(str(db_user.id))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=db_user.id,
        )

    async def refresh_user_token(self, refresh_token: RequestToken) -> TokenResponse:
        try:
            token_payload = await self.jwt.verify_token(refresh_token)
        except ValueError as e:
            logger.info(f"Invalid token: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")

        db_user = await self.repository.get(id=int(token_payload.sub))
        if not db_user:
            logger.info(f"Invalid user in token: {token_payload}")
            raise HTTPException(status_code=401, detail="Invalid token")
        access_token = await self.jwt.create_access_token(str(db_user.id))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token.token,
            user_id=db_user.id,
        )
