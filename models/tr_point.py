from __future__ import annotations

from datetime import datetime  # noqa: TCH003

from pydantic import BaseModel


class TrPoint(BaseModel):
    instrument: str
    datetime: datetime
    value: float


class AtrPoint(BaseModel):
    instrument: str
    datetime: datetime
    value: int
