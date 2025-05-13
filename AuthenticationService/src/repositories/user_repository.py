from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.base_repository import AbstractRepository
from src.schemas.user import SerializedUser
from src.tables.user import User


class UsersRepository(AbstractRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(
            self,
            **kwargs: dict,
    ) -> User | None:
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
        allowed_columns = {"id", "email", "login"}

        if column not in allowed_columns:
            raise ValueError("Invalid column")

        result = await self.session.execute(
            select(User)
            .where(getattr(User, column) == value),
        )
        return result.scalars().first()


    async def add(
            self,
            user: SerializedUser,
    ) -> User.id:
        result = await self.session.execute(
            insert(User)
            .values(
                login=user.login,
                hashed_password=user.hashed_password,
            )
            .returning(User.id),
        )
        await self.session.commit()
        return result.scalar()

    async def set_email(
            self,
            email: str,
            user_id: int,
    ) -> User:
        result = await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(email=email)
            .returning(User),
        )
        await self.session.commit()
        return result.scalar()



    async def list(
            self,
            offset: int,
            limit: int,
    ) -> list[User]:
        result = await self.session.execute(
            select(User)
            .offset(offset)
            .limit(limit),
        )
        return result.scalars().all()

    async def delete(
            self,
            user_id: int,
    ) -> User:
        result = await self.session.execute(
            delete(User)
            .where(User.id == user_id)
            .returning(User),
        )
        await self.session.commit()
        return result.scalar()

