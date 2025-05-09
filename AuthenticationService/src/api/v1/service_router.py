from fastapi import APIRouter

from src.core.config import settings

router = APIRouter(
    prefix=settings.api.v1.root,
    tags=["Service"],
)

# for application healthcheck
@router.get("/ping")
async def ping() -> None:
    return None
