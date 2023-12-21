from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.api.dependencies import record_service
from app.core.services import RecordService

router = APIRouter(prefix="/pages", tags=["pages"])
templates = Jinja2Templates(directory="app/api/templates")


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@router.get("/records")
async def records(request: Request, service: RecordService = Depends(record_service)):
    lst = await service.paginate(1, 10)

    return templates.TemplateResponse(
        "records.html", {"request": request, "records": lst}
    )


@router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
