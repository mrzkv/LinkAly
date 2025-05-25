from .redirect_router import router as redirect_router
from .service_router import router as service_router

routers = [
    service_router,
    redirect_router,
]
