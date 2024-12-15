from __future__ import annotations

from datetime import datetime  # noqa: TCH003

from pydantic import BaseModel


class LongBalancePoint(BaseModel):
    instrument: str
    datetime: datetime
    balance: list[float]
