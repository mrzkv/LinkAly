from abc import abstractmethod


class BaseMiddleware:

    @abstractmethod
    def install(self) -> None:
        ...
