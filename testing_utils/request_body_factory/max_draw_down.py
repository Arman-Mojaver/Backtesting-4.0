from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_validator

from database.models import LongOperationPoint, ShortOperationPoint
from testing_utils.finance_utils.draw_down import calculate_max_draw_down
from testing_utils.operation_points_utils.utils import generate_weekdays
from utils.date_utils import datetime_to_string


class StrategyDataMaxDrawDown(BaseModel):
    max_draw_down: float
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


class StrategyResponseMaxDrawDown(BaseModel):
    strategy_data: StrategyDataMaxDrawDown
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

    def __eq__(self, other: StrategyResponseMaxDrawDown):
        if isinstance(other, StrategyResponseMaxDrawDown):
            return (
                self.strategy_data == other.strategy_data
                and frozenset(self.long_operation_point_ids)
                == frozenset(other.long_operation_point_ids)
                and frozenset(self.short_operation_point_ids)
                == frozenset(other.short_operation_point_ids)
            )
        return False


class MaxDrawDownRequestBodyFactory:
    ID_GAP = 701

    def __init__(  # noqa: PLR0913
        self,
        instrument: str,
        mm_strategy_id: int,
        start_date: str,
        end_date: str,
        long_signals: list[list[str]],
        short_signals: list[list[str]],
        long_results: list[int],
        long_tps: list[int],
        long_sls: list[int],
        short_results: list[int],
        short_tps: list[int],
        short_sls: list[int],
    ):
        self.instrument: str = instrument
        self.mm_strategy_id: int = mm_strategy_id
        self.start_date: str = start_date
        self.end_date: str = end_date
        self.long_signals: list[list[str]] = long_signals
        self.short_signals: list[list[str]] = short_signals
        self.long_results: list[int] = long_results
        self.long_tps: list[int] = long_tps
        self.long_sls: list[int] = long_sls
        self.short_results: list[int] = short_results
        self.short_tps: list[int] = short_tps
        self.short_sls: list[int] = short_sls

        self.body = self.generate_body()

    def generate_body(self) -> dict[str, Any]:
        long_operation_points, short_operation_points = (
            self._generate_operation_points_list()
        )
        long_operation_points_dict, short_operation_points_dict, dates_str = (
            self._generate_operation_points_dict(
                long_operation_points,
                short_operation_points,
            )
        )
        signals_dict = self._generate_signals_dict()

        return {
            "money_management_strategy_id": self.mm_strategy_id,
            "long_operation_points": long_operation_points_dict,
            "short_operation_points": short_operation_points_dict,
            "signals": signals_dict,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

    def _generate_operation_points_list(
        self,
    ) -> tuple[list[LongOperationPoint], list[ShortOperationPoint]]:
        long_operation_points, short_operation_points = [], []

        start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()  # noqa: DTZ007
        end_date = datetime.strptime(self.end_date, "%Y-%m-%d").date()  # noqa: DTZ007
        dates = generate_weekdays(start_date=start_date, end_date=end_date)

        for index, date in enumerate(dates):
            result = self.long_results[index]
            tp = self.long_tps[index]
            sl = self.long_sls[index]

            long_operation_point = LongOperationPoint(
                instrument=self.instrument,
                datetime=date,
                result=result,
                tp=tp,
                sl=sl,
                long_balance=[],
                risk=0.02,
                money_management_strategy_id=self.mm_strategy_id,
            )
            long_operation_points.append(long_operation_point)

        for index, date in enumerate(dates):
            result = self.short_results[index]
            tp = self.short_tps[index]
            sl = self.short_sls[index]

            short_operation_point = ShortOperationPoint(
                instrument=self.instrument,
                datetime=date,
                result=result,
                tp=tp,
                sl=sl,
                short_balance=[],
                risk=0.02,
                money_management_strategy_id=self.mm_strategy_id,
            )
            short_operation_points.append(short_operation_point)

        for index, point in enumerate(long_operation_points + short_operation_points, 1):
            point.id = index

        return long_operation_points, short_operation_points

    @staticmethod
    def _generate_operation_points_dict(  # noqa: ANN205
        long_operation_points: list[LongOperationPoint],
        short_operation_points: list[ShortOperationPoint],
    ):
        long_operation_points_dict = {
            datetime_to_string(point.datetime): point.to_request_format()
            for point in long_operation_points
        }
        short_operation_points_dict = {
            datetime_to_string(point.datetime): point.to_request_format()
            for point in short_operation_points
        }

        dates_str = tuple(long_operation_points_dict.keys())
        return long_operation_points_dict, short_operation_points_dict, dates_str

    def _generate_signals_dict(self):
        signals = defaultdict(dict)
        for index, (long_signals, short_signals) in enumerate(
            zip(
                self.long_signals,
                self.short_signals,
                strict=True,
            )
        ):
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

    def strategy_responses(self) -> list[StrategyResponseMaxDrawDown]:
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

                strategy_data = StrategyDataMaxDrawDown(
                    max_draw_down=calculate_max_draw_down(
                        operation_items=operations_points
                    ),
                    money_management_strategy_id=mm_strategy_id,
                    indicator_id=indicator_id,
                )

                strategy_response = StrategyResponseMaxDrawDown(
                    strategy_data=strategy_data,
                    long_operation_point_ids=long_operation_point_ids,
                    short_operation_point_ids=short_operation_point_ids,
                )

                strategy_responses.append(strategy_response)

        return strategy_responses
