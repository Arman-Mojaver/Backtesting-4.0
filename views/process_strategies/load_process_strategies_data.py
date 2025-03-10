from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from database.models import LongOperationPoint, ShortOperationPoint


class InvalidOperationPointsError(Exception):
    pass


@dataclass
class OperationPoints:
    long_operation_points: dict[int, list[LongOperationPoint]]
    short_operation_points: dict[int, list[ShortOperationPoint]]

    def __eq__(self, other: OperationPoints) -> bool:
        """
        Return True if two instances have the same long_operation_point IDs
        and short_operation_point IDs. Used exclusively in tests.
        """
        if (
            self.long_operation_points.keys() != other.long_operation_points.keys()
            or self.short_operation_points.keys() != other.short_operation_points.keys()
        ):
            return False

        for mm_strategy_id, operation_points in self.long_operation_points.items():
            if {point.id for point in operation_points} != {
                point.id for point in other.long_operation_points[mm_strategy_id]
            }:
                return False

        for mm_strategy_id, operation_points in self.short_operation_points.items():
            if {point.id for point in operation_points} != {
                point.id for point in other.short_operation_points[mm_strategy_id]
            }:
                return False

        return True


class LoadProcessStrategiesData:
    def __init__(self, instrument: str):
        self.instrument = instrument

    def run(self) -> OperationPoints:
        long_operation_point_by_mm_strategies = (
            LongOperationPoint.query.from_instrument_by_mm_strategy(
                instrument=self.instrument,
            )
        )
        short_operation_point_by_mm_strategies = (
            ShortOperationPoint.query.from_instrument_by_mm_strategy(
                instrument=self.instrument,
            )
        )

        self._validate_operation_points(
            long_operation_point_by_mm_strategies,
            short_operation_point_by_mm_strategies,
        )

        return OperationPoints(
            long_operation_point_by_mm_strategies,
            short_operation_point_by_mm_strategies,
        )

    @staticmethod
    def _check_equal_date_sets(list_of_sets: list[set[Any]]) -> bool:
        first_set = list_of_sets[0]
        return all(s == first_set for s in list_of_sets)

    def _validate_operation_points(
        self,
        long_operation_point_by_mm_strategies: dict[str, list[LongOperationPoint]],
        short_operation_point_by_mm_strategies: dict[str, list[ShortOperationPoint]],
    ) -> None:
        long_dates = [
            {point.datetime for point in long_operation_points}
            for long_operation_points in long_operation_point_by_mm_strategies.values()
        ]

        short_dates = [
            {point.datetime for point in short_operation_points}
            for short_operation_points in short_operation_point_by_mm_strategies.values()
        ]

        valid_operation_points = (
            long_dates
            and short_dates
            and self._check_equal_date_sets(long_dates + short_dates)
        )

        if not valid_operation_points:
            err = "There were mismatches between long and short operation points"
            raise InvalidOperationPointsError(err)
