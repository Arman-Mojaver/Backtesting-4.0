from __future__ import annotations

from collections import defaultdict
from typing import Any

from sqlalchemy import ARRAY, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base, CRUDMixin, session


class LongOperationPointQuery:
    @staticmethod
    def all() -> list[LongOperationPoint]:
        return list(session.query(LongOperationPoint).all())

    @staticmethod
    def from_instrument(instrument: str) -> list[LongOperationPoint]:
        return list(
            session.query(LongOperationPoint).filter_by(instrument=instrument).all()
        )

    @staticmethod
    def from_instrument_by_mm_strategy(
        instrument: str,
    ) -> dict[str, list[LongOperationPoint]]:
        points = list(
            session.query(LongOperationPoint).filter_by(instrument=instrument).all()
        )
        points_by_mm_strategy = defaultdict(list)
        for point in points:
            points_by_mm_strategy[point.money_management_strategy_id].append(point)

        return points_by_mm_strategy


class LongOperationPoint(Base, CRUDMixin):
    __tablename__ = "long_operation_point"
    __repr_fields__ = ("instrument", "datetime", "money_management_strategy_id")
    serialize_rules = ("-id", "-money_management_strategy_id", "-strategies")

    query = LongOperationPointQuery

    id = Column(Integer, primary_key=True, autoincrement=True)
    instrument = Column(String, nullable=False)
    datetime = Column(Date, nullable=False)
    result = Column(Integer, nullable=False)
    tp = Column(Integer, nullable=False)
    sl = Column(Integer, nullable=False)
    long_balance = Column(ARRAY(Integer), nullable=False)
    risk = Column(Float, nullable=False)
    money_management_strategy_id = Column(
        Integer,
        ForeignKey("money_management_strategy.id"),
        nullable=False,
    )
    strategies = relationship(
        "Strategy",
        back_populates="long_operation_points",
        secondary="long_operation_points_strategies",
    )

    def to_request_format(self) -> dict[str, Any]:
        return self.to_dict(rules=("id", "money_management_strategy_id", "-long_balance"))
