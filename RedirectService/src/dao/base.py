from abc import ABC, abstractmethod


class AbstractDAO(ABC):
    @abstractmethod
    async def get(self, **kwargs: dict) -> object: ...

    @abstractmethod
    async def add(self, obj: object) -> object: ...

    @abstractmethod
    async def delete(self, obj_id: int) -> object: ...
