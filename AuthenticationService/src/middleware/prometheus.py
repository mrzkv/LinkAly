from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.core.config import settings
from src.middleware.base import AbstractMiddleware


class Prometheus(AbstractMiddleware):
    def __init__(
            self,
            app: FastAPI,
    ) -> None:
        self.app = app

    def install(self) -> None:
        (
            Instrumentator()
             .instrument(self.app)
             .expose(
                self.app,
                endpoint=f"{settings.api.v1.root}/metrics",
                tags=["Service"],
            )
        )
