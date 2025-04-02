from __future__ import annotations

from collections import defaultdict
from typing import Any

from sqlalchemy import ARRAY, Column, Date, Float, ForeignKey, Integer, String

from database import Base, CRUDMixin, session


class ShortOperationPointQuery:
    @staticmethod
    def all() -> list[ShortOperationPoint]:
        return list(session.query(ShortOperationPoint).all())

    @staticmethod
    def from_instrument(instrument: str) -> list[ShortOperationPoint]:
        return list(
            session.query(ShortOperationPoint).filter_by(instrument=instrument).all()
        )

    @staticmethod
    def from_instrument_by_mm_strategy(
        instrument: str,
    ) -> dict[str, list[ShortOperationPoint]]:
        points = list(
            session.query(ShortOperationPoint).filter_by(instrument=instrument).all()
        )
        points_by_mm_strategy = defaultdict(list)
        for point in points:
            points_by_mm_strategy[point.money_management_strategy_id].append(point)

        return points_by_mm_strategy

    @staticmethod
    def from_ids_by_id(ids: list[int]) -> dict[int, ShortOperationPoint]:
        short_operation_points_by_id = {}
        short_operation_points = list(
            session.query(ShortOperationPoint)
            .filter(ShortOperationPoint.id.in_(ids))
            .all()
        )
        for point in short_operation_points:
            short_operation_points_by_id[point.id] = point

        return short_operation_points_by_id


class ShortOperationPoint(Base, CRUDMixin):
    __tablename__ = "short_operation_point"
    __repr_fields__ = ("instrument", "datetime", "money_management_strategy_id")
    serialize_rules = ("-id", "-money_management_strategy_id", "-strategies")

    query = ShortOperationPointQuery

    id = Column(Integer, primary_key=True, autoincrement=True)
    instrument = Column(String, nullable=False)
    datetime = Column(Date, nullable=False)
    result = Column(Integer, nullable=False)
    tp = Column(Integer, nullable=False)
    sl = Column(Integer, nullable=False)
    short_balance = Column(ARRAY(Integer), nullable=False)
    risk = Column(Float, nullable=False)
    money_management_strategy_id = Column(
        Integer,
        ForeignKey("money_management_strategy.id"),
        nullable=False,
    )

    def to_request_format(self) -> dict[str, Any]:
        return self.to_dict(
            rules=("id", "money_management_strategy_id", "-short_balance")
        )
