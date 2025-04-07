from __future__ import annotations

from typing import TYPE_CHECKING, Any

from models.operation_point import OperationPoints
from utils.dict_utils import dict_multi_by_key

if TYPE_CHECKING:
    from database.models import LongOperationPoint, ShortOperationPoint


class InvalidOperationPointsError(Exception):
    pass


class OperationPointsValidator:
    def __init__(
        self,
        long_operation_points: list[LongOperationPoint],
        short_operation_points: list[ShortOperationPoint],
    ):
        self.long_operation_points: list[LongOperationPoint] = long_operation_points
        self.short_operation_points: list[ShortOperationPoint] = short_operation_points

    def run(self) -> OperationPoints:
        self._validate_instruments()
        long_operation_points_by_mm_strategy = dict_multi_by_key(
            self.long_operation_points,
            key="money_management_strategy_id",
        )
        short_operation_points_by_mm_strategy = dict_multi_by_key(
            self.short_operation_points,
            key="money_management_strategy_id",
        )
        self._validate_dates_and_money_management_strategies(
            long_operation_points_by_mm_strategy, short_operation_points_by_mm_strategy
        )

        return OperationPoints(
            long_operation_points=self.long_operation_points,
            short_operation_points=self.short_operation_points,
        )

    def _validate_instruments(self):
        long_instruments = {point.instrument for point in self.long_operation_points}
        short_instruments = {point.instrument for point in self.short_operation_points}
        if long_instruments != short_instruments:
            err = "There were mismatches between long and short operation points"
            raise InvalidOperationPointsError(err)

    @staticmethod
    def _check_equal_date_sets(list_of_sets: list[set[Any]]) -> bool:
        first_set = list_of_sets[0]
        return all(s == first_set for s in list_of_sets)

    def _validate_dates_and_money_management_strategies(
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
