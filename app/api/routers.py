from app.api.auth.router import router as auth_router
from app.api.pages.router import router as pages_router
from app.api.records.router import router as record_router

routers = (record_router, auth_router, pages_router)
