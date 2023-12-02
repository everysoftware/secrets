import datetime
import enum
from html import escape as e

from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    def dump(self):
        dump = self.model_dump()

        for key, value in dump.items():
            if value is None:
                dump[key] = "нет"
            elif isinstance(value, datetime.datetime):
                dump[key] = value.strftime("%d-%m-%Y %H:%M")
            elif isinstance(value, str):
                dump[key] = e(value)
            elif isinstance(value, enum.Enum):
                dump[key] = value.name

        return dump
