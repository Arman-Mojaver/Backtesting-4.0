from __future__ import annotations

from sqlalchemy import Column, Integer

from database import Base, CRUDMixin, session


class ShortOperationPointQuery:
    @staticmethod
    def all() -> list[ShortOperationPointStrategy]:
        return list(session.query(ShortOperationPointStrategy).all())


class ShortOperationPointStrategy(Base, CRUDMixin):
    __tablename__ = "short_operation_points_strategies"
    __repr_fields__ = ("short_operation_point_id", "strategy_id")
    serialize_rules = ("-short_operation_point_id", "-strategy_id")

    query = ShortOperationPointQuery

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_operation_point_id = Column(Integer, nullable=False)
    strategy_id = Column(Integer, nullable=False)
