from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.middleware.prometheus import PrometheusMiddleware


def register_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        PrometheusMiddleware,
    )
