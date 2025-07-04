from __future__ import annotations

from datetime import datetime  # noqa: TCH003 (used by pydantic schema)

from pydantic import BaseModel, ConfigDict, field_serializer, field_validator

from utils.date_utils import datetime_to_string, string_to_datetime


class RawPointD1Schema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    instrument: str
    datetime: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

    @field_validator("datetime", mode="before")
    @classmethod
    def deserialize_datetime(cls, value: str) -> datetime:  # type: ignore[valid-type]
        return string_to_datetime(value)

    @field_serializer("datetime")
    def serialize_datetime(self, value: datetime) -> str:  # type: ignore[valid-type]
        """Only used to serialize in tests."""
        return datetime_to_string(value)
