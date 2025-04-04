from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, field_validator

from schemas.raw_points_schema import (
    RawPointsSchema,  # noqa: TCH001 (used by pydantic schema)
)
from utils.list_utils import list_items_are_equal

if TYPE_CHECKING:
    from schemas.raw_point_d1_schema import RawPointD1Schema
    from schemas.raw_point_h1_schema import RawPointH1Schema


class EnabledInstrumentsMismatchError(Exception):
    """
    Error raised when the instruments in the file
    and the enabled instruments do not match.
    """


class InstrumentsSchema(BaseModel):
    data: dict[str, RawPointsSchema] = {}

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

    def validate_instruments_enabled(self, enabled_instruments: tuple[str, ...]) -> None:
        if set(enabled_instruments) != set(self.data.keys()):
            err = (
                f"Mismatch between enabled instruments and file instruments: "
                f"{enabled_instruments=}, {self.data.keys()=}"
            )
            raise EnabledInstrumentsMismatchError(err)

    def raw_points_d1(self) -> list[RawPointD1Schema]:
        return [
            raw_point_d1
            for raw_points_schema in self.data.values()
            for raw_point_d1 in raw_points_schema.raw_points_d1
        ]

    def raw_points_h1(self) -> list[RawPointH1Schema]:
        return [
            raw_point_h1
            for raw_points_schema in self.data.values()
            for raw_point_h1 in raw_points_schema.raw_points_h1
        ]
