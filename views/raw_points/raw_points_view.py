from __future__ import annotations

from collections import defaultdict
from typing import Any

from pydantic import ValidationError

from config import config  # type: ignore[attr-defined]
from config.logging_config.log_decorators import log_on_end, log_on_start
from database.models import RawPointD1, RawPointH1
from schemas.instruments_schema import InstrumentsSchema


class RawPointsCreateMultipleView:
    def __init__(
        self,
        data: dict[str, Any],
        enabled_instruments: tuple[str, ...] = config.ENABLED_INSTRUMENTS,
    ):
        self.data: dict[str, Any] = data
        self.enabled_instruments = enabled_instruments
        self.instruments_data: InstrumentsSchema = InstrumentsSchema()
        self.raw_points_d1_by_instrument_by_date: defaultdict[Any, dict] = defaultdict(
            dict
        )

    @log_on_end("Finished RawPointsCreateMultipleView")
    def run(self) -> list[RawPointD1]:
        self.instruments_data = self._get_instrument_data()
        self.instruments_data.validate_instruments_enabled(
            enabled_instruments=self.enabled_instruments,
        )
        self._create_raw_d1_points()
        self._create_raw_h1_points()

        return [
            point
            for points_by_date in self.raw_points_d1_by_instrument_by_date.values()
            for point in points_by_date.values()
        ]

    def _get_instrument_data(self):
        try:
            return InstrumentsSchema(**self.data)
        except ValidationError:
            raise

    @log_on_start("Creating RawPointD1 points")
    def _create_raw_d1_points(self):
        for raw_point_d1_data in self.instruments_data.raw_points_d1():
            raw_point_d1 = RawPointD1(**raw_point_d1_data.model_dump())
            self.raw_points_d1_by_instrument_by_date[raw_point_d1.instrument][
                raw_point_d1.datetime
            ] = raw_point_d1

    @log_on_start("Creating RawPointH1 points")
    def _create_raw_h1_points(self):
        for raw_point_h1_data in self.instruments_data.raw_points_h1():
            raw_point_h1 = RawPointH1(**raw_point_h1_data.model_dump())
            self.raw_points_d1_by_instrument_by_date[raw_point_h1_data.instrument][
                raw_point_h1_data.date_str()
            ].raw_points_h1.append(raw_point_h1)
