from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path

from app.api.auth.base_config import current_user, two_fa_verified
from app.core.enums import UserRole
from app.core.models import User
from app.core.services import RecordService
from .schemes import RecordCreate, RecordRead, RecordsRead, RecordUpdate
from ..dependencies import record_service

router = APIRouter(prefix="/records", tags=["records"])


@router.post("/create", response_model=RecordRead, status_code=201)
async def create_record(
        record: RecordCreate,
        service: RecordService = Depends(record_service),
):
    return await service.create(record)


@router.get(
    "/{id}",
    response_model=RecordRead,
    responses={
        404: {"description": "Record not found"},
        403: {"description": "Not enough rights"},
    },
    dependencies=[Depends(two_fa_verified)],
)
async def get_record(
        id: Annotated[int, Path(ge=1)],  # noqa E501
        user: User = Depends(current_user),
        service: RecordService = Depends(record_service),
):
    obj = await service.get(id)

    if obj is None:
        raise HTTPException(status_code=404, detail="Record not found")
    if obj.user_id != user.id and user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough rights")

    return obj


@router.get("/count")
async def count_records(service: RecordService = Depends(record_service)):
    return await service.count()


@router.get("", response_model=RecordsRead)
async def paginate_records(
        page: int = 1, per_page: int = 10, service: RecordService = Depends(record_service)
):
    total = await service.count()
    pages = total // per_page + (total % per_page > 0)

    if page > pages:
        raise HTTPException(status_code=404, detail="Page not found")

    records = await service.paginate(page, per_page)

    return RecordsRead(
        items=records,
        total=total,
        page=page,
        pages=pages,
        per_page=per_page,
    )


@router.patch(
    "/{id}",
    response_model=RecordRead,
    responses={
        404: {"description": "Record not found"},
        403: {"description": "Not enough rights"},
    },
    dependencies=[Depends(two_fa_verified)],
)
async def patch_record(
        id: Annotated[int, Path(ge=1)],  # noqa E501
        record: RecordUpdate,
        user: User = Depends(two_fa_verified),
        service: RecordService = Depends(record_service),
):
    obj = await service.get(id)

    if obj is None:
        raise HTTPException(status_code=404, detail="Record not found")
    if obj.user_id != user.id and user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough rights")

    await service.update(id, record)

    return obj


@router.delete(
    "/{id}",
    responses={
        404: {"description": "Record not found"},
        403: {"description": "Not enough rights"},
    },
)
async def delete_record(
        id: Annotated[int, Path(ge=1)],  # noqa E501
        user: User = Depends(two_fa_verified),
        service: RecordService = Depends(record_service),
):
    obj = await service.get(id)

    if obj is None:
        raise HTTPException(status_code=404, detail="Record not found")
    if obj.user_id != user.id and user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough rights")

    await service.delete(id)

    return {"detail": "Record deleted successfully"}
