from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer

from database import Base, CRUDMixin


class LongOperationPointStrategy(Base, CRUDMixin):
    __tablename__ = "long_operation_points_strategies"
    __repr_fields__ = ("long_operation_point_id", "strategy_id")
    serialize_rules = ("-long_operation_point_id", "-strategy_id")

    id = Column(Integer, primary_key=True, autoincrement=True)
    long_operation_point_id = Column(
        Integer,
        ForeignKey("long_operation_point.id"),
        nullable=False,
    )
    strategy_id = Column(
        Integer,
        ForeignKey("strategy.id"),
        nullable=False,
    )
