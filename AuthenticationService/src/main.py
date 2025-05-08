import uvicorn
from fastapi import FastAPI

from src.api.general_router import register_routers
from src.core.config import env_settings
from src.core.lifespan import lifespan
from src.middleware.general_middleware import register_middleware

app = FastAPI(lifespan=lifespan)

register_middleware(app)
register_routers(app)


def start_server() -> None:
    uvicorn.run(
        app="main:app",
        host=env_settings.IP_ADDRESS,
        port=env_settings.PORT,
        workers=env_settings.UVICORN_WORKERS,
    )

if __name__ == "__main__":
    start_server()
