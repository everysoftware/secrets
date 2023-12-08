from app.api.auth.router import router as auth_router
from app.api.records.router import router as record_router

routers = (
    record_router,
    auth_router,
)
