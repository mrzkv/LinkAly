from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user_repository import UsersRepository
from src.schemas.user import SerializedUser, TokenResponse, UserCreate
from src.security.argon_hasher import ArgonHasher
from src.security.jwt import AuthJWT


class UserService:
    def __init__(self, session: AsyncSession, jwt: AuthJWT = AuthJWT()) -> None:
        self.repository = UsersRepository(session)
        self.jwt = jwt

    async def register_user(self,
                            user: UserCreate,
                            hasher: ArgonHasher = ArgonHasher()
    ) -> TokenResponse:
        if await self.repository.get(login=user.login):
            raise ValueError("Login already exists")
        serialized_user = SerializedUser(
            login=user.login,
            hashed_password=await hasher.hash_password(user.password),
        )
        user_id = await self.repository.add(serialized_user)
        access_token = await self.jwt.create_access_token(str(user_id))
        refresh_token = await self.jwt.create_refresh_token(str(user_id))
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user_id,
        )
