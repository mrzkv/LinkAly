from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from repositories.base import T
from src.repositories.base import AbstractRepository
from src.tables.user import User
from src.schemas.user import UserCreate

class UsersRepository(AbstractRepository[User]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(User)
            .where(User.id == user_id)
            .limit(1)
        )
        return result.scalar()

    async def add(self, user: UserCreate) -> User:
        result = await self.session.execute(
            insert(User)
            .values(
                user.login,
                user.password
            )
            .returning(User)
        )
        await self.session.commit()
        return result.scalar()

    async def list(self, offset: int, limit: int) -> list[User]:
        result = await self.session.execute(
            select(User)
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    async def delete(self, user_id: int) -> User:
        result = await self.session.execute(
            delete(User)
            .where(User.id == user_id)
            .returning(User)
        )
        await self.session.commit()
        return result.scalar()
