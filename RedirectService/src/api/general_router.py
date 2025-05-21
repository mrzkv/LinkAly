from fastapi import FastAPI

from src.api.v1.service_router import router as service_router


def register_routers(app: FastAPI) -> None:
    app.include_router(service_router)
