from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import JSONResponse

from src.core.config import settings

router = APIRouter(
    prefix=settings.api.v1.root,
    tags=["Service"],
)

# endpoint for application healthcheck
@router.get("/health")
async def ping() -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
        },
    )

# endpoint for prometheus metrics
@router.get("/metrics")
async def get_metrics_for_prometheus() -> Response:
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )

