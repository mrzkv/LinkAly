from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.db_helper import db_helper
from src.core.logging_promtail import logger


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



