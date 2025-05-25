from abc import abstractmethod


class AbstractMiddleware:

    @abstractmethod
    def install(self) -> None:
        ...
