from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    try:
        yield
    except Exception as e:
        # logger.error(f"during startup: {e}")
        print(e)
    finally:
        try:
            pass
            # await engine_dispose()
        except Exception as e:
            # logger.error(f"during shutdown: {e}")
            print(e)
