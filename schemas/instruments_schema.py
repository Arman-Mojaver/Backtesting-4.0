from __future__ import annotations

from pydantic import BaseModel, field_validator

from schemas.raw_points_schema import (
    RawPointsSchema,  # noqa: TCH001 (used by pydantic schema)
)
from utils.list_utils import list_items_are_equal


class InstrumentsSchema(BaseModel):
    data: dict[str, RawPointsSchema]

    @field_validator("data", mode="after")
    @classmethod
    def validate_instruments(
        cls,
        data: dict[str, RawPointsSchema],
    ) -> dict[str, RawPointsSchema]:
        for instrument, raw_points_schema in data.items():
            if not raw_points_schema.instruments_match(instrument):
                err = "Mismatch between instrument data"
                raise ValueError(err)

        return data

    @field_validator("data", mode="after")
    @classmethod
    def validate_end_dates(
        cls,
        data: dict[str, RawPointsSchema],
    ) -> dict[str, RawPointsSchema]:
        all_end_dates = [
            raw_points_schema.end_date() for raw_points_schema in data.values()
        ]
        if not list_items_are_equal(all_end_dates):
            err = "Mismatch between end dates"
            raise ValueError(err)

        return data
