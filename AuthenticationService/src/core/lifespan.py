from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1 import routers
from src.core.db_helper import db_helper
from src.core.logging_promtail import logger
from src.middleware import middlewares


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    try:
        yield
    except Exception as e:
        logger.error(f"during startup: {e}")
    finally:
        try:
            await db_helper.dispose()
        except Exception as e:
            logger.error(f"during shutdown: {e}")



def register_middlewares(app: FastAPI) -> None:
    for middleware in middlewares:
        middleware(app).install()

def register_routers(app: FastAPI) -> None:
    for router in routers:
        app.include_router(router)
