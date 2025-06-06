import uvicorn
from fastapi import FastAPI

from src.core.config import settings
from src.core.lifespan import lifespan, register_middlewares, register_routers

app = FastAPI(lifespan=lifespan)

register_middlewares(app)
register_routers(app)


def start_server() -> None:
    uvicorn.run(
        app="main:app",
        host=settings.server.host,
        port=settings.server.port,
        workers=settings.server.uvicorn_workers,
    )

if __name__ == "__main__":
    start_server()
