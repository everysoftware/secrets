import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DecryptedRecord:
    id: int
    title: str
    username: str
    password: str
    url: Optional[str]
    comment: Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
