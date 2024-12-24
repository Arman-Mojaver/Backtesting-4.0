from __future__ import annotations

from collections import defaultdict
from datetime import datetime  # noqa: TCH003

from pydantic import BaseModel


class FluctuationPoint(BaseModel):
    datetime: datetime
    value: int


class BaseBalancePoint(BaseModel):
    instrument: str
    datetime: datetime
    balance: list[FluctuationPoint]

    def balance_values(self) -> list[int]:
        return [point.value for point in self.balance]


class LongBalancePoint(BaseBalancePoint):
    pass


class ShortBalancePoint(BaseBalancePoint):
    @classmethod
    def from_long_balance_point(
        cls,
        long_balance_point: LongBalancePoint,
    ) -> ShortBalancePoint:
        balance = [
            FluctuationPoint(datetime=point.datetime, value=-point.value)
            for point in long_balance_point.balance
        ]
        return cls(
            datetime=long_balance_point.datetime,
            instrument=long_balance_point.instrument,
            balance=balance,
        )


class BaseBalancePoints(BaseModel):
    items: list[BaseBalancePoint] = []

    def by_date(self) -> dict[datetime, BaseBalancePoint]:
        result: dict[datetime, BaseBalancePoint] = defaultdict()
        for point in self.items:
            result[point.datetime] = point
        return result


class LongBalancePoints(BaseBalancePoints):
    pass


class ShortBalancePoints(BaseBalancePoints):
    @classmethod
    def from_long_balance_points(
        cls,
        long_balance_points: LongBalancePoints,
    ) -> ShortBalancePoints:
        return cls(
            items=[
                ShortBalancePoint.from_long_balance_point(item)
                for item in long_balance_points.items
            ]
        )
