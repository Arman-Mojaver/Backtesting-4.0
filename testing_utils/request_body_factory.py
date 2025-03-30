from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Any

from testing_utils.finance_utils.utils import get_lists_evenly_spaced_samples
from testing_utils.operation_points_utils import (
    generate_random_long_operation_points,
    generate_random_short_operation_points,
)
from utils.date_utils import datetime_to_string

if TYPE_CHECKING:
    from database.models import LongOperationPoint, ShortOperationPoint


class ProcessStrategiesRequestBodyFactory:
    ID_GAP = 701

    def __init__(  # noqa: PLR0913
        self,
        instrument: str,
        mm_strategy_count: int,
        start_date: str,
        end_date: str,
        long_signals_counts: list[int],
        short_signals_counts: list[int],
    ):
        self.instrument: str = instrument
        self.mm_strategy_count: int = mm_strategy_count
        self.start_date: str = start_date
        self.end_date: str = end_date
        self.long_signals_counts: list[int] = long_signals_counts
        self.short_signals_counts: list[int] = short_signals_counts

        self._validate_signals_counts()

        self.body = self.generate_body()

    def _validate_signals_counts(self) -> None:
        if len(self.long_signals_counts) != len(self.short_signals_counts):
            err = (
                "long_signals_counts and short_signals_counts "
                "can not have different lengths"
            )
            raise ValueError(err)

    def generate_body(self) -> dict[str, Any]:
        long_operation_points, short_operation_points = (
            self._generate_operation_points_list()
        )
        operation_points_dict, dates_str = self._generate_operation_points_dict(
            long_operation_points,
            short_operation_points,
        )
        signals_dict = self._generate_signals_dict(dates_str)

        return {
            "operation_points": operation_points_dict,
            "signals": signals_dict,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

    def _generate_operation_points_list(
        self,
    ) -> tuple[list[LongOperationPoint], list[ShortOperationPoint]]:
        long_operation_points, short_operation_points = [], []
        for money_management_strategy_id in range(1, self.mm_strategy_count + 1):
            points = generate_random_long_operation_points(
                money_management_strategy_id=money_management_strategy_id,
                instrument=self.instrument,
                start_date=self.start_date,
                end_date=self.end_date,
            )
            long_operation_points.extend(points)

        for money_management_strategy_id in range(1, self.mm_strategy_count + 1):
            points = generate_random_short_operation_points(
                money_management_strategy_id=money_management_strategy_id,
                instrument=self.instrument,
                start_date=self.start_date,
                end_date=self.end_date,
            )
            short_operation_points.extend(points)

        for index, point in enumerate(long_operation_points + short_operation_points, 1):
            point.id = index

        return long_operation_points, short_operation_points

    @staticmethod
    def _generate_operation_points_dict(  # noqa: ANN205
        long_operation_points: list[LongOperationPoint],
        short_operation_points: list[ShortOperationPoint],
    ):
        operation_points = defaultdict(lambda: defaultdict(dict))
        for point in long_operation_points:
            operation_points[point.money_management_strategy_id]["long_operation_points"][
                datetime_to_string(point.datetime)
            ] = point.to_request_format()

        for point in short_operation_points:
            operation_points[point.money_management_strategy_id][
                "short_operation_points"
            ][datetime_to_string(point.datetime)] = point.to_request_format()

        dates_str = tuple(operation_points[1]["long_operation_points"].keys())
        return operation_points, dates_str

    def _generate_signals_dict(self, dates_str: tuple[str, ...]):
        signals = defaultdict(dict)
        for index, (long_count, short_count) in enumerate(
            zip(
                self.long_signals_counts,
                self.short_signals_counts,
                strict=True,
            )
        ):
            long_signals, short_signals = get_lists_evenly_spaced_samples(
                dates_str,
                long_count,
                short_count,
            )
            indicator_id = index + self.ID_GAP

            signals[indicator_id]["long_signals"] = long_signals
            signals[indicator_id]["short_signals"] = short_signals

        return signals

    def mm_strategy_ids(self) -> list[int]:
        return list(self.body["operation_points"].keys())

    def indicator_ids(self) -> list[int]:
        return list(self.body["signals"].keys())

    def strategy_ids(self) -> set[tuple[int, int]]:
        return {
            (mm_strategy_id, indicator_id)
            for mm_strategy_id in self.mm_strategy_ids()
            for indicator_id in self.indicator_ids()
        }

    def strategy_count(self) -> int:
        return len(self.mm_strategy_ids()) * len(self.indicator_ids())
