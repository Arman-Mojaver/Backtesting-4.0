from __future__ import annotations

from datetime import datetime  # noqa: TCH003

from database.models import (
    LongOperationPoint,
    MoneyManagementStrategy,
    ResampledPointD1,
    ShortOperationPoint,
)
from database.models.resasmpled_point_d1 import HighLowOrder
from models.balance_point import (
    FluctuationPoint,
    LongBalancePoint,
    LongBalancePoints,
    ShortBalancePoint,
    ShortBalancePoints,
)
from models.tr_point import AtrPoint, TrPoint


class OperationPointsCreateOneController:
    def __init__(
        self,
        money_management_strategy: MoneyManagementStrategy,
        resampled_points: list[ResampledPointD1],
    ):
        self.money_management_strategy: MoneyManagementStrategy = (
            money_management_strategy
        )
        self.resampled_points: list[ResampledPointD1] = resampled_points
        self.atr_parameter = self.money_management_strategy.parameters["atr_parameter"]

        self.long_balance_points: LongBalancePoints = LongBalancePoints()
        self.short_balance_points: ShortBalancePoints = ShortBalancePoints()
        self.long_balance_points_by_date: dict[datetime, LongBalancePoint] = {}
        self.short_balance_points_by_date: dict[datetime, ShortBalancePoint] = {}
        self.tr_points: list[TrPoint] = []
        self.atr_points: list[AtrPoint] = []
        self.long_operation_points: list[LongOperationPoint] = []
        self.short_operation_points: list[ShortOperationPoint] = []

    def run(self) -> tuple[list[LongOperationPoint], list[ShortOperationPoint]]:
        self.long_balance_points = self._get_long_balance_points()
        self.short_balance_points = ShortBalancePoints.from_long_balance_points(
            long_balance_points=self.long_balance_points,
        )
        self.long_balance_points_by_date = self.long_balance_points.by_date()
        self.short_balance_points_by_date = self.short_balance_points.by_date()
        self.tr_points = self._get_tr_points()
        self.atr_points = self._get_atr_points()
        self.long_operation_points = self._get_long_operation_points()
        self.short_operation_points = self._get_short_operation_points()
        self._filter_out_balance_overflow_results()

        return self.long_operation_points, self.short_operation_points

    def _get_long_balance_points(self) -> LongBalancePoints:
        long_balance_points = []
        for open_point_index, open_point in enumerate(self.resampled_points):
            long_balance = self._generate_long_balance(
                open_point_index=open_point_index,
                open_point=open_point,
                resampled_points=self.resampled_points,
            )

            long_balance_point = LongBalancePoint(
                instrument=open_point.instrument,
                datetime=open_point.datetime,
                balance=long_balance,
            )

            long_balance_points.append(long_balance_point)
        return LongBalancePoints(items=long_balance_points)

    def _generate_long_balance(
        self,
        open_point_index: int,
        open_point: ResampledPointD1,
        resampled_points: list[ResampledPointD1],
    ) -> list[FluctuationPoint]:
        long_balance: list[FluctuationPoint] = []
        for high_low_point in resampled_points[open_point_index:]:
            if self._is_high_or_undefined(point=high_low_point):
                self._high_first(
                    open_point=open_point,
                    high_low_point=high_low_point,
                    long_balance=long_balance,
                )
            else:
                self._low_first(
                    open_point=open_point,
                    high_low_point=high_low_point,
                    long_balance=long_balance,
                )
        return long_balance

    @staticmethod
    def _is_high_or_undefined(point: ResampledPointD1) -> bool:
        return point.high_low_order in {HighLowOrder.high_first, HighLowOrder.undefined}

    @staticmethod
    def _low_first(
        open_point: ResampledPointD1,
        high_low_point: ResampledPointD1,
        long_balance: list[FluctuationPoint],
    ) -> None:
        long_balance.append(
            FluctuationPoint(
                datetime=high_low_point.datetime,
                value=int(round(10000 * (-open_point.open + high_low_point.low))),
            )
        )
        long_balance.append(
            FluctuationPoint(
                datetime=high_low_point.datetime,
                value=int(round(10000 * (-open_point.open + high_low_point.high))),
            )
        )

    @staticmethod
    def _high_first(
        open_point: ResampledPointD1,
        high_low_point: ResampledPointD1,
        long_balance: list[FluctuationPoint],
    ) -> None:
        long_balance.append(
            FluctuationPoint(
                datetime=high_low_point.datetime,
                value=int(round(10000 * (-open_point.open + high_low_point.high))),
            )
        )
        long_balance.append(
            FluctuationPoint(
                datetime=high_low_point.datetime,
                value=int(round(10000 * (-open_point.open + high_low_point.low))),
            )
        )

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
        balance: list[FluctuationPoint],
    ) -> int | None:
        for balance_point in balance:
            if balance_point.value >= tp:
                return tp

            if balance_point.value <= -sl:
                return -sl

        # Balance overflow
        return None

    def _get_long_operation_points(self) -> list[LongOperationPoint]:
        long_operation_points: list[LongOperationPoint] = []
        for atr_point in self.atr_points:
            tp = round(atr_point.value * self.money_management_strategy.tp_multiplier)
            sl = round(atr_point.value * self.money_management_strategy.sl_multiplier)
            long_balance_point = self.long_balance_points_by_date[atr_point.datetime]
            result = self._calculate_result(
                tp=tp,
                sl=sl,
                balance=long_balance_point.balance,
            )
            long_operation_point = LongOperationPoint(
                instrument=atr_point.instrument,
                datetime=atr_point.datetime,
                result=result,
                tp=tp,
                sl=sl,
                long_balance=long_balance_point.balance_values(),
                money_management_strategy_id=self.money_management_strategy.id,
            )
            long_operation_points.append(long_operation_point)

        return long_operation_points

    def _get_short_operation_points(self) -> list[ShortOperationPoint]:
        short_operation_points: list[ShortOperationPoint] = []
        for atr_point in self.atr_points:
            tp = round(atr_point.value * self.money_management_strategy.tp_multiplier)
            sl = round(atr_point.value * self.money_management_strategy.sl_multiplier)
            short_balance_point = self.short_balance_points_by_date[atr_point.datetime]

            result = self._calculate_result(
                tp=tp,
                sl=sl,
                balance=short_balance_point.balance,
            )

            short_operation_point = ShortOperationPoint(
                instrument=atr_point.instrument,
                datetime=atr_point.datetime,
                result=result,
                tp=tp,
                sl=sl,
                short_balance=short_balance_point.balance_values(),
                money_management_strategy_id=self.money_management_strategy.id,
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
