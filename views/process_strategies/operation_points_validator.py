from __future__ import annotations

from typing import TYPE_CHECKING

from models.operation_point import OperationPoints

if TYPE_CHECKING:
    from database.models import LongOperationPoint, ShortOperationPoint


class InvalidOperationPointsError(Exception):
    pass


class OperationPointsValidator:
    def __init__(
        self,
        money_management_strategy_id: int,
        long_operation_points: list[LongOperationPoint],
        short_operation_points: list[ShortOperationPoint],
    ):
        self.money_management_strategy_id: int = money_management_strategy_id
        self.long_operation_points: list[LongOperationPoint] = long_operation_points
        self.short_operation_points: list[ShortOperationPoint] = short_operation_points

    def run(self) -> OperationPoints:
        self._validate_operation_points()
        self._validate_instruments()
        self._validate_dates()
        self._validate_money_management_strategy_ids()
        return OperationPoints(
            long_operation_points=self.long_operation_points,
            short_operation_points=self.short_operation_points,
        )

    def _validate_operation_points(self):
        if not self.long_operation_points or not self.short_operation_points:
            err = (
                f"There were missing operation points: "
                f"{self.long_operation_points=}, {self.short_operation_points=}"
            )
            raise InvalidOperationPointsError(err)

    def _validate_instruments(self):
        long_instruments = {point.instrument for point in self.long_operation_points}
        short_instruments = {point.instrument for point in self.short_operation_points}
        if long_instruments != short_instruments:
            err = "There were mismatches between long and short operation points"
            raise InvalidOperationPointsError(err)

    def _validate_dates(self):
        long_dates = {point.datetime for point in self.long_operation_points}
        short_dates = {point.datetime for point in self.short_operation_points}
        if long_dates != short_dates:
            err = (
                "There were date mismatches between long and short operation points"
                f"{long_dates=}, {short_dates=}"
            )
            raise InvalidOperationPointsError(err)

    def _validate_money_management_strategy_ids(self):
        long_money_management_strategy_ids = {
            point.money_management_strategy_id for point in self.long_operation_points
        }
        short_money_management_strategy_ids = {
            point.money_management_strategy_id for point in self.short_operation_points
        }
        if long_money_management_strategy_ids != short_money_management_strategy_ids:
            err = (
                "There were money_management_strategy_id mismatches between "
                "long and short operation points"
                f"{long_money_management_strategy_ids=}, "
                f"{short_money_management_strategy_ids=}"
            )
            raise InvalidOperationPointsError(err)
