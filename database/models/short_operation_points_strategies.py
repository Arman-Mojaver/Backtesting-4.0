from __future__ import annotations

from sqlalchemy import Column, Integer

from database import Base, CRUDMixin


class ShortOperationPointStrategy(Base, CRUDMixin):
    __tablename__ = "short_operation_points_strategies"
    __repr_fields__ = ("short_operation_point_id", "strategy_id")
    serialize_rules = ("-short_operation_point_id", "-strategy_id")

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_operation_point_id = Column(Integer, nullable=False)
    strategy_id = Column(Integer, nullable=False)
