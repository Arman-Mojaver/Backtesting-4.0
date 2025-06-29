from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Index, Integer

from database import Base, CRUDMixin


class ShortOperationPointStrategy(Base, CRUDMixin):
    __tablename__ = "short_operation_points_strategies"
    __repr_fields__ = ("id", "short_operation_point_id", "strategy_id")
    __table_args__ = (
        Index(
            "ix_short_operation_point_strategy_strategy_id",
            "strategy_id",
        ),
    )

    serialize_rules = ("-id",)

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_operation_point_id = Column(
        Integer,
        ForeignKey("short_operation_point.id", ondelete="CASCADE"),
        nullable=False,
    )
    strategy_id = Column(
        Integer,
        ForeignKey("strategy.id", ondelete="CASCADE"),
        nullable=False,
    )
