import time
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import Request, Response
from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware

type CallNext = Callable[[Request], Awaitable[Response]]

request_count = Counter(
"http_requests_total",
"Total HTTP requests",
["method", "endpoint", "status_code"],
)
request_latency = Histogram(
"http_request_latency_seconds",
"Request latency in seconds",
["method", "endpoint"],
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> None:
        super().__init__(*args, **kwargs)

    async def dispatch(
            self,
            request: Request,
            call_next: CallNext,
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        request_count.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code,
        ).inc()

        request_latency.labels(
            method=request.method,
            endpoint=request.url.path,
        ).observe(process_time)

        return response
