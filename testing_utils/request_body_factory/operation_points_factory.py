from __future__ import annotations

from typing import TYPE_CHECKING

from testing_utils.operation_points_utils.long_operation_points import (
    generate_random_long_operation_points,
)
from testing_utils.operation_points_utils.short_operation_points import (
    generate_random_short_operation_points,
)

if TYPE_CHECKING:
    from database.models import LongOperationPoint, ShortOperationPoint


class OperationPoints(list):
    def to_request_format(self) -> list[LongOperationPoint | ShortOperationPoint]:
        return [item.to_request_format() for item in self]


class OperationPointsFactory:
    def __init__(
        self,
        instrument: str,
        mm_strategy_id: int,
        start_date: str,
        end_date: str,
    ):
        self.instrument: str = instrument
        self.mm_strategy_id: int = mm_strategy_id
        self.start_date: str = start_date
        self.end_date: str = end_date

        self.long_operation_points, self.short_operation_points = (
            self._generate_long_short_operation_points_list()
        )
        self.operation_points = self._generate_operation_points_list()

    def _generate_operation_points_list(self) -> OperationPoints:
        operation_points = []
        for index, (long_point, short_point) in enumerate(
            zip(self.long_operation_points, self.short_operation_points, strict=True)
        ):
            if index % 2 == 0:
                operation_points.append(long_point)
            else:
                operation_points.append(short_point)

        return OperationPoints(operation_points)

    def _generate_long_short_operation_points_list(
        self,
    ) -> tuple[list[LongOperationPoint], list[ShortOperationPoint]]:
        long_operation_points = generate_random_long_operation_points(
            money_management_strategy_id=self.mm_strategy_id,
            instrument=self.instrument,
            start_date=self.start_date,
            end_date=self.end_date,
        )

        short_operation_points = generate_random_short_operation_points(
            money_management_strategy_id=self.mm_strategy_id,
            instrument=self.instrument,
            start_date=self.start_date,
            end_date=self.end_date,
        )

        for index, point in enumerate(long_operation_points + short_operation_points, 1):
            point.id = index

        return long_operation_points, short_operation_points

    def get_evenly_spaced(self, count: int) -> OperationPoints:
        if count > len(self.operation_points):
            err = "Count can not be greater than generated operation_points"
            raise ValueError(err)

        if count == 0:
            return OperationPoints([])

        if count == len(self.operation_points):
            return OperationPoints(self.operation_points)

        step = int(len(self.operation_points) / count)

        operation_points = self.operation_points[::step][:count]

        if count != len(operation_points):
            err = "Mismatch on count and operation_points size"
            raise ValueError(err)

        return OperationPoints(operation_points)


class OperationPointsFromDataFactory:
    def __init__(
        self,
        instrument: str,
        mm_strategy_id: int,
        start_date: str,
        data: tuple[tuple[int, int, int], ...],
    ):
        self.instrument: str = instrument
        self.mm_strategy_id: int = mm_strategy_id
        self.start_date: str = start_date
        self.data: tuple[tuple[int, int, int], ...] = data
        self.count: int = len(data)

        self.long_operation_points, self.short_operation_points = (
            self._generate_long_short_operation_points_list()
        )
        self.operation_points = self._generate_operation_points_list()

    def _generate_operation_points_list(self) -> OperationPoints:
        operation_points = []
        for index, (long_point, short_point) in enumerate(
            zip(self.long_operation_points, self.short_operation_points, strict=True)
        ):
            if index % 2 == 0:
                operation_points.append(long_point)
            else:
                operation_points.append(short_point)

        return OperationPoints(operation_points)

    def _generate_long_short_operation_points_list(
        self,
    ) -> tuple[list[LongOperationPoint], list[ShortOperationPoint]]:
        long_operation_points = generate_random_long_operation_points(
            money_management_strategy_id=self.mm_strategy_id,
            instrument=self.instrument,
            start_date=self.start_date,
            count=self.count,
        )

        short_operation_points = generate_random_short_operation_points(
            money_management_strategy_id=self.mm_strategy_id,
            instrument=self.instrument,
            start_date=self.start_date,
            count=self.count,
        )

        for index, point in enumerate(long_operation_points + short_operation_points, 1):
            point.id = index

        return long_operation_points, short_operation_points

    def operation_points_from_data(self) -> OperationPoints:
        if len(self.data) != len(self.operation_points):
            err = "Mismatch between data and operation points sizes"
            raise ValueError(err)

        for index, (result, tp, sl) in enumerate(self.data):
            self.operation_points[index].result = result
            self.operation_points[index].tp = tp
            self.operation_points[index].sl = sl

        return OperationPoints(self.operation_points)
