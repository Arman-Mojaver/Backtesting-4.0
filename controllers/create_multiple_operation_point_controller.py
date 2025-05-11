from __future__ import annotations

from datetime import date  # noqa: TCH003

from database.models import (
    LongOperationPoint,
    MoneyManagementStrategy,
    ResampledPointD1,
    ShortOperationPoint,
)
from models.tr_point import AtrPoint, TrPoint
from utils.date_utils import datetime_to_string


class OperationPointsCreateOneController:
    def __init__(
        self,
        money_management_strategy: MoneyManagementStrategy,
        resampled_points: list[ResampledPointD1],
        long_balance_points_by_date: dict[date, list[int]],
        short_balance_points_by_date: dict[date, list[int]],
    ):
        self.money_management_strategy: MoneyManagementStrategy = (
            money_management_strategy
        )
        self.resampled_points: list[ResampledPointD1] = resampled_points
        self.atr_parameter = self.money_management_strategy.parameters["atr_parameter"]

        self.long_balance_points_by_date: dict[date, list[int]] = (
            long_balance_points_by_date
        )
        self.short_balance_points_by_date: dict[date, list[int]] = (
            short_balance_points_by_date
        )

        self.tr_points: list[TrPoint] = []
        self.atr_points: list[AtrPoint] = []
        self.long_operation_points: list[LongOperationPoint] = []
        self.short_operation_points: list[ShortOperationPoint] = []

    def run(self) -> tuple[list[LongOperationPoint], list[ShortOperationPoint]]:
        self.tr_points = self._get_tr_points()
        self.atr_points = self._get_atr_points()
        self.long_operation_points = self._get_long_operation_points()
        self.short_operation_points = self._get_short_operation_points()
        self._filter_out_balance_overflow_results()

        return self.long_operation_points, self.short_operation_points

    def _get_tr_points(self) -> list[TrPoint]:
        initial_point = self.resampled_points[0]
        tr_points = [
            TrPoint(
                instrument=initial_point.instrument,
                datetime=initial_point.datetime,
                value=initial_point.high - initial_point.low,
            )
        ]

        for index, point in enumerate(self.resampled_points[1:], 1):
            previous_point = self.resampled_points[index - 1]
            tr_value = max(
                point.high - point.low,
                abs(point.high - previous_point.close),
                abs(point.low - previous_point.close),
            )
            tr_point = TrPoint(
                instrument=point.instrument,
                datetime=point.datetime,
                value=tr_value,
            )
            tr_points.append(tr_point)

        return tr_points

    def _get_atr_points(self) -> list[AtrPoint]:
        result_length = len(self.tr_points) + 1 - self.atr_parameter
        atr_points = []
        for index in range(result_length):
            true_range_sub_points = self.tr_points[index : index + self.atr_parameter]
            applicable_point = true_range_sub_points[-1]
            sum_true_range_values = sum(
                [tr_point.value for tr_point in true_range_sub_points]
            )
            atr_value = int(round(10000 * sum_true_range_values / self.atr_parameter))
            atr_points.append(
                AtrPoint(
                    instrument=applicable_point.instrument,
                    datetime=applicable_point.datetime,
                    value=atr_value,
                )
            )
        return atr_points

    @staticmethod
    def _calculate_result(
        tp: int,
        sl: int,
        balance: list[int],
    ) -> tuple[int | None, list[int]]:
        for balance_index, balance_value in enumerate(balance):
            if balance_value >= tp:
                return tp, balance[: balance_index + 1]

            if balance_value <= -sl:
                return -sl, balance[: balance_index + 1]

        # Balance overflow
        return None, []

    def _get_long_operation_points(self) -> list[LongOperationPoint]:
        long_operation_points: list[LongOperationPoint] = []
        for atr_point in self.atr_points:
            tp = round(atr_point.value * self.money_management_strategy.tp_multiplier)
            sl = round(atr_point.value * self.money_management_strategy.sl_multiplier)
            long_balance = self.long_balance_points_by_date[atr_point.datetime.date()]
            result, partial_long_balance = self._calculate_result(
                tp=tp,
                sl=sl,
                balance=long_balance,
            )
            long_operation_point = LongOperationPoint(
                instrument=atr_point.instrument,
                datetime=datetime_to_string(atr_point.datetime),
                result=result,
                tp=tp,
                sl=sl,
                long_balance=partial_long_balance,
                money_management_strategy_id=self.money_management_strategy.id,
                risk=self.money_management_strategy.risk,
                timestamp=int(atr_point.datetime.timestamp()),
            )
            long_operation_points.append(long_operation_point)

        return long_operation_points

    def _get_short_operation_points(self) -> list[ShortOperationPoint]:
        short_operation_points: list[ShortOperationPoint] = []
        for atr_point in self.atr_points:
            tp = round(atr_point.value * self.money_management_strategy.tp_multiplier)
            sl = round(atr_point.value * self.money_management_strategy.sl_multiplier)
            short_balance = self.short_balance_points_by_date[atr_point.datetime.date()]

            result, partial_short_balance = self._calculate_result(
                tp=tp,
                sl=sl,
                balance=short_balance,
            )

            short_operation_point = ShortOperationPoint(
                instrument=atr_point.instrument,
                datetime=datetime_to_string(atr_point.datetime),
                result=result,
                tp=tp,
                sl=sl,
                short_balance=partial_short_balance,
                money_management_strategy_id=self.money_management_strategy.id,
                risk=self.money_management_strategy.risk,
                timestamp=int(atr_point.datetime.timestamp()),
            )
            short_operation_points.append(short_operation_point)

        return short_operation_points

    def _filter_out_balance_overflow_results(self):
        filtered_long_operation_points, filtered_short_operation_points = [], []
        for long_point, short_point in zip(
            self.long_operation_points,
            self.short_operation_points,
            strict=True,
        ):
            if long_point.result is None or short_point.result is None:
                break

            filtered_long_operation_points.append(long_point)
            filtered_short_operation_points.append(short_point)

        self.long_operation_points = filtered_long_operation_points
        self.short_operation_points = filtered_short_operation_points
