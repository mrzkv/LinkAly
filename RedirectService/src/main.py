import uvicorn
from fastapi import FastAPI

from src.api.general_router import register_routers
from src.core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

register_routers(app)


def start_server() -> None:
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        workers=3,
    )

if __name__ == "__main__":
    start_server()
