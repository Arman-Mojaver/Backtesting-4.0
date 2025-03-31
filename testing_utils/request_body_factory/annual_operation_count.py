from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, field_validator

from testing_utils.finance_utils.annual_operation_count import (
    calculate_annual_operation_count,
)
from testing_utils.finance_utils.utils import get_lists_evenly_spaced_samples
from testing_utils.operation_points_utils.long_operation_points import (
    generate_random_long_operation_points,
)
from testing_utils.operation_points_utils.short_operation_points import (
    generate_random_short_operation_points,
)
from utils.date_utils import datetime_to_string

if TYPE_CHECKING:
    from database.models import LongOperationPoint, ShortOperationPoint


class StrategyDataOperationCount(BaseModel):
    annual_operation_count: float
    money_management_strategy_id: int
    indicator_id: int

    def __hash__(self):
        return hash(
            (
                self.annual_operation_count,
                self.money_management_strategy_id,
                self.indicator_id,
            )
        )


class StrategyResponseOperationCount(BaseModel):
    strategy_data: StrategyDataOperationCount
    long_operation_point_ids: list[int] | None
    short_operation_point_ids: list[int] | None

    @field_validator(
        "long_operation_point_ids",
        "short_operation_point_ids",
        mode="before",
    )
    @classmethod
    def none_to_empty_list(cls, value: list[int] | None) -> list[int]:
        if value is None:
            return []
        return value

    def __hash__(self):
        return hash(
            (
                hash(self.strategy_data),
                frozenset(self.long_operation_point_ids),
                frozenset(self.short_operation_point_ids),
            )
        )

    def __eq__(self, other: StrategyResponseOperationCount):
        if isinstance(other, StrategyResponseOperationCount):
            return (
                self.strategy_data == other.strategy_data
                and frozenset(self.long_operation_point_ids)
                == frozenset(other.long_operation_point_ids)
                and frozenset(self.short_operation_point_ids)
                == frozenset(other.short_operation_point_ids)
            )
        return False


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
        return sorted(self.body["operation_points"].keys())

    def indicator_ids(self) -> list[int]:
        return sorted(self.body["signals"].keys())

    def strategy_ids(self) -> set[tuple[int, int]]:
        return {
            (mm_strategy_id, indicator_id)
            for mm_strategy_id in self.mm_strategy_ids()
            for indicator_id in self.indicator_ids()
        }

    def strategy_count(self) -> int:
        return len(self.mm_strategy_ids()) * len(self.indicator_ids())

    def strategy_responses(self) -> list[StrategyResponseOperationCount]:
        strategy_responses = []
        for mm_strategy_id in self.mm_strategy_ids():
            for indicator_id in self.indicator_ids():
                long_signals = self.body["signals"][indicator_id]["long_signals"]
                short_signals = self.body["signals"][indicator_id]["short_signals"]
                all_long_operation_points = self.body["operation_points"][mm_strategy_id][
                    "long_operation_points"
                ]
                all_short_operation_points = self.body["operation_points"][
                    mm_strategy_id
                ]["short_operation_points"]
                long_operation_points = [
                    all_long_operation_points[signal] for signal in long_signals
                ]
                short_operation_points = [
                    all_short_operation_points[signal] for signal in short_signals
                ]
                operations_points = sorted(
                    long_operation_points + short_operation_points,
                    key=lambda x: x["datetime"],
                )

                long_operation_point_ids = [
                    point["id"] for point in long_operation_points
                ]
                short_operation_point_ids = [
                    point["id"] for point in short_operation_points
                ]

                strategy_data = StrategyDataOperationCount(
                    annual_operation_count=calculate_annual_operation_count(
                        operation_items=operations_points,
                        start_date=self.start_date,
                        end_date=self.end_date,
                    ),
                    money_management_strategy_id=mm_strategy_id,
                    indicator_id=indicator_id,
                )

                strategy_response = StrategyResponseOperationCount(
                    strategy_data=strategy_data,
                    long_operation_point_ids=long_operation_point_ids,
                    short_operation_point_ids=short_operation_point_ids,
                )

                strategy_responses.append(strategy_response)

        return strategy_responses
