from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.config import CorsConfig, settings

from src.middleware.base import AbstractMiddleware


class CORS(AbstractMiddleware):
    def __init__(
            self,
            app: FastAPI,
            config: CorsConfig = settings.cors,
    ) -> None:
        self.app = app
        self.allowed = config

    def install(self) -> None:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.allowed.origins,
            allow_credentials=self.allowed.credentials,
            allow_methods=self.allowed.methods,
            allow_headers=self.allowed.headers,
        )
