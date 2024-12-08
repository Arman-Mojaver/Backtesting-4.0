from __future__ import annotations

from sqlalchemy.exc import SQLAlchemyError

from config.logging_config.log_decorators import log_on_end, log_on_start
from database import session
from database.models import RawPointD1, RawPointH1, ResampledPointD1


class NoRawPointsError(Exception):
    """Error raised when there are not RawPointD1 or RawPointH1."""


class ResampledPointsCreateMultipleView:
    def __init__(self):
        self.raw_points_d1: list[RawPointD1] = []

    @log_on_end("Finished ResampledPointsCreateMultipleView")
    def run(self) -> None:
        self.raw_points_d1 = RawPointD1.query.all()
        self._validate_raw_points_d1_exist()
        self._validate_raw_points_h1_exist()
        self._create_resampled_points()
        self._commit()

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

    @log_on_start("Creating ResampledPointD1 points")
    def _create_resampled_points(self) -> None:
        for raw_point_d1 in self.raw_points_d1:
            resampled_point = ResampledPointD1(
                high_low_order=raw_point_d1.high_low_order(),
                **raw_point_d1.to_dict(),
            )
            session.add(resampled_point)

    @staticmethod
    @log_on_end("Committed")
    def _commit() -> None:
        try:
            session.commit()
        except SQLAlchemyError:
            session.rollback()
        finally:
            session.close()
