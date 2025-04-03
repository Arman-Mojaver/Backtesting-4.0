from __future__ import annotations

from sqlalchemy import Column, Integer

from database import Base, CRUDMixin, session


class LongOperationPointQuery:
    @staticmethod
    def all() -> list[LongOperationPointStrategy]:
        return list(session.query(LongOperationPointStrategy).all())


class LongOperationPointStrategy(Base, CRUDMixin):
    __tablename__ = "long_operation_points_strategies"
    __repr_fields__ = ("long_operation_point_id", "strategy_id")
    serialize_rules = ("-long_operation_point_id", "-strategy_id")

    query = LongOperationPointQuery

    id = Column(Integer, primary_key=True, autoincrement=True)
    long_operation_point_id = Column(Integer, nullable=False)
    strategy_id = Column(Integer, nullable=False)
