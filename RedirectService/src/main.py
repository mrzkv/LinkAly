import uvicorn
from fastapi import FastAPI

from src.api.general_router import register_routers
from src.core.config import settings
from src.core.lifespan import lifespan
from src.middlewares.general_middleware import register_middlewares

app = FastAPI(lifespan=lifespan)

register_routers(app)
register_middlewares(app)

def start_server() -> None:
    uvicorn.run(
        app="main:app",
        host=settings.server.host,
        port=settings.server.port,
        workers=settings.server.workers,
    )

if __name__ == "__main__":
    start_server()
