from __future__ import annotations

from config.logging_config.log_decorators import log_on_end, log_on_start
from database.models import RawPointD1, RawPointH1, ResampledPointD1
from utils.date_utils import string_to_datetime


class NoRawPointsError(Exception):
    """Error raised when there are not RawPointD1 or RawPointH1."""


class ResampledPointsCreateMultipleView:
    def __init__(self, raw_points_d1: list[RawPointD1]):
        self.raw_points_d1: list[RawPointD1] = raw_points_d1

    @log_on_start("Creating ResampledPointD1 points")
    @log_on_end("Finished ResampledPointsCreateMultipleView")
    def run(self) -> list[ResampledPointD1]:
        self._validate_raw_points_d1_exist()
        self._validate_raw_points_h1_exist()
        return self._create_resampled_points()

    def _validate_raw_points_d1_exist(self) -> None:
        self._validate_points_exist(points=self.raw_points_d1)

    def _validate_raw_points_h1_exist(self) -> None:
        for raw_point_d1 in self.raw_points_d1:
            self._validate_points_exist(points=raw_point_d1.raw_points_h1)

    @staticmethod
    def _validate_points_exist(points: list[RawPointD1] | list[RawPointH1]) -> None:
        if not points:
            err = "No raw points in database"
            raise NoRawPointsError(err)

    def _create_resampled_points(self) -> list[ResampledPointD1]:
        return [
            ResampledPointD1(
                high_low_order=raw_point_d1.high_low_order(),
                timestamp=int(string_to_datetime(str(raw_point_d1.datetime)).timestamp()),
                **raw_point_d1.to_dict(),
            )
            for raw_point_d1 in self.raw_points_d1
        ]
