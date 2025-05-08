from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, text

from repositories.base import T
from src.repositories.base import AbstractRepository
from src.tables.user import User
from src.schemas.user import UserCreate

class UsersRepository(AbstractRepository[User]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, **kwargs) -> Optional[User]:
        """
        This function takes positional arguments
        and executes the query with them.

        >>> id = 1
        'SELECT * FROM users WHERE id = 1'
        >>> login = mrzkv
        'SELECT * FROM users WHERE login = mrzkv'
        >>> email = mrzkv@tech.com
        'SELECT * FROM users WHERE email = mrzkv@tech.com'
        """

        if len(kwargs.keys()) != 1:
            raise ValueError("Only 1 positional argument is allowed")

        column, value = next(iter(kwargs.items()))
        allowed_columns = {'id', 'email', 'login'}

        if column not in allowed_columns:
            raise ValueError("Invalid column")

        result = await self.session.execute(
            text(f"SELECT * FROM users WHERE {colums} = :value LIMIT 1 "),
            {'value': value}
        )
        return result.scalar_one_or_none()


    async def add(self, obj: User) -> User:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj


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

