from .recovery_router import router as recovery_router
from .service_router import router as service_router
from .users_router import router as users_router

routers = (
    service_router,
    users_router,
    recovery_router,
)
