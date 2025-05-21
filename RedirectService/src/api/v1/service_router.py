from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.core.config import settings

router = APIRouter(
    prefix=settings.api.v1.root,
    tags=["Service"],
)

# endpoint for application health check
@router.get("/health")
def get_health() -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
        },
    )
