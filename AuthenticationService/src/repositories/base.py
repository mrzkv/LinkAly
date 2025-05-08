from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

T = TypeVar("T")

class AbstractRepository(ABC, Generic[T]):

    @abstractmethod
    async def get(self, **kwargs) -> Optional[T]:
        """
        This function takes positional arguments
        and executes the query with them.
        """
        pass

    @abstractmethod
    async def list(self, limit: int, offset: int) -> List[T]:
        pass

    @abstractmethod
    async def add(self, obj: T) -> T:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass