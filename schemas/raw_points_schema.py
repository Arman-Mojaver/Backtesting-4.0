from __future__ import annotations

from datetime import datetime  # noqa: TCH003 (used by pydantic schema)
from typing import Self

from pydantic import BaseModel, model_validator

from schemas.raw_point_d1_schema import (
    RawPointD1Schema,  # noqa: TCH001 (used by pydantic schema)
)
from schemas.raw_point_h1_schema import (
    RawPointH1Schema,  # noqa: TCH001 (used by pydantic schema)
)


class RawPointsSchema(BaseModel):
    raw_points_d1: list[RawPointD1Schema]
    raw_points_h1: list[RawPointH1Schema]

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        raw_points_h1_dates = {
            dt.replace(hour=0, minute=0, second=0, microsecond=0)
            for dt in self._raw_points_h1_datetimes()
        }

        if raw_points_h1_dates != self._raw_points_d1_dates():
            err = "Mismatch between instrument dates"
            raise ValueError(err)

        return self

    def _raw_points_d1_dates(self) -> set[datetime]:
        return {point.datetime for point in self.raw_points_d1}

    def _raw_points_h1_datetimes(self) -> set[datetime]:
        return {point.datetime for point in self.raw_points_h1}

    def instruments_match(self, instrument: str) -> bool:
        raw_points_d1_instruments = [item.instrument for item in self.raw_points_d1]
        raw_points_h1_instruments = [item.instrument for item in self.raw_points_h1]

        instruments = [*raw_points_d1_instruments, *raw_points_h1_instruments]

        return all(instrument == item for item in instruments)

    def end_date(self) -> datetime:
        return max(self._raw_points_d1_dates())
