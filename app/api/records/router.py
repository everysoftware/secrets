from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from app.api.auth.base_config import current_user, two_fa_verified
from app.api.utils import AES
from app.core import Database, get_database
from app.core.config import cfg
from app.core.enums import UserRole
from app.core.models import Comment, Record, User

from .schemes import RecordCreate, RecordRead, RecordsRead, RecordUpdate

router = APIRouter(prefix="/records", tags=["records"])


@router.post("/create", response_model=RecordRead, status_code=201)
async def create_record(
    record: RecordCreate,
    user: User = Depends(two_fa_verified),
    db: Database = Depends(get_database),
):
    obj = Record(
        user_id=user.id,
        name=record.name,
        username=AES.encrypt(record.username, cfg.api.secret_encryption),
        password=AES.encrypt(record.password, cfg.api.secret_encryption),
        url=record.url,
    )

    if record.comment is not None:
        comment = Comment(**record.comment.model_dump())
        db.session.add(comment)
        obj.comment = comment

    obj = db.record.new(obj)
    await db.session.commit()

    return obj


@router.get(
    "/{id}",
    response_model=RecordRead,
    responses={
        404: {"description": "Record not found"},
        403: {"description": "Not enough rights"},
    },
)
async def get_record(
    id: Annotated[int, Path(ge=1)],  # noqa E501
    db: Database = Depends(get_database),
    user: User = Depends(two_fa_verified),
):
    obj = await db.record.get(id, options=[joinedload(Record.comment)])  # noqa E501
    if obj is None:
        raise HTTPException(status_code=404, detail="Record not found")
    if obj.user_id != user.id and user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough rights")

    return obj


async def count_records(db: Database, user_id: int) -> int:
    stmt = select(func.count(Record.id)).where(Record.user_id == user_id)
    res = await db.session.execute(stmt)
    count = res.scalar_one()

    return count


@router.get("", response_model=RecordsRead)
async def paginate_records(
    page: Annotated[int, Path(ge=1)] = 1,
    per_page: Annotated[int, Path(ge=1)] = 10,
    db: Database = Depends(get_database),
    user: User = Depends(current_user),
):
    stmt = (
        select(Record)
        .where(Record.user_id == user.id)
        .order_by(Record.name)
        .options(joinedload(Record.comment))  # noqa E501
    )
    offset = (page - 1) * per_page
    stmt = stmt.limit(per_page).offset(offset)
    result = await db.session.execute(stmt)
    records = result.scalars().all()

    return RecordsRead(
        items=records,
        total=await count_records(db, user.id),
        page=page,
        per_page=per_page,
    )


@router.patch(
    "/{id}",
    response_model=RecordRead,
    responses={
        404: {"description": "Record not found"},
        403: {"description": "Not enough rights"},
    },
)
async def patch_record(
    id: Annotated[int, Path(ge=1)],  # noqa E501
    record: RecordUpdate,
    db: Database = Depends(get_database),
    user: User = Depends(current_user),
):
    obj = await db.record.get(id, options=[joinedload(Record.comment)])  # noqa E501
    if obj is None:
        raise HTTPException(status_code=404, detail="Record not found")
    if obj.user_id != user.id and user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough rights")

    if record.name is not None:
        obj.name = record.name
    if record.username is not None:
        obj.username = AES.encrypt(record.username, cfg.api.secret_encryption)
    if record.password is not None:
        obj.password = AES.encrypt(record.password, cfg.api.secret_encryption)
    if record.url is not None:
        obj.url = record.url

    if record.comment is not None and record.comment.text is not None:
        if obj.comment is None:
            obj.comment = db.comment.new(Comment(**record.comment.model_dump()))
            await db.record.merge(obj)
        else:
            comment = obj.comment
            comment.text = record.comment.text
            await db.comment.merge(comment)

    await db.session.commit()

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
    db: Database = Depends(get_database),
    user: User = Depends(current_user),
):
    obj = await db.record.get(id, options=[joinedload(Record.comment)])  # noqa E501
    if obj is None:
        raise HTTPException(status_code=404, detail="Record not found")
    if obj.user_id != user.id and user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough rights")
    await db.record.delete(obj)
    await db.session.commit()

    return {"detail": "Record deleted successfully"}
