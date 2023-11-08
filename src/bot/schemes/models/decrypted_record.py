from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DecryptedRecord:
    title: str
    username: str
    password: str
    url: Optional[str]
    comment: Optional[str]
