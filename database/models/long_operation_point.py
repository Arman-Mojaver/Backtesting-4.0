from __future__ import annotations

from typing import Any

from sqlalchemy import ARRAY, Column, Date, Float, ForeignKey, Integer, String

from database import Base, CRUDMixin, session


class LongOperationPointQuery:
    @staticmethod
    def all() -> list[Any]:
        return list(session.query(LongOperationPoint).all())


class LongOperationPoint(Base, CRUDMixin):
    __tablename__ = "long_operation_point"
    __repr_fields__ = ("instrument", "datetime", "money_management_strategy_id")
    serialize_rules = ("-id", "-money_management_strategy_id")

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
