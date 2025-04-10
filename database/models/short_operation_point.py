from __future__ import annotations

from typing import Any

from sqlalchemy import ARRAY, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Query

from database import Base, CRUDMixin, session


class ShortOperationPointQuery(Query):
    pass


class ShortOperationPoint(Base, CRUDMixin):
    __tablename__ = "short_operation_point"
    __repr_fields__ = ("instrument", "datetime", "money_management_strategy_id")
    serialize_rules = ("-id", "-money_management_strategy_id", "-strategies")

    query: ShortOperationPointQuery = session.query_property(
        query_cls=ShortOperationPointQuery
    )

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
