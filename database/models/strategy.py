from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, Query, object_session, relationship

from database import Base, CRUDMixin, session

if TYPE_CHECKING:
    from database.models import (
        Indicator,
        LongOperationPoint,
        MoneyManagementStrategy,
        ShortOperationPoint,
    )


class StrategyQuery(Query):
    @staticmethod
    def distinct_money_management_strategy_ids() -> set[int]:
        return {
            row[0]
            for row in session.query(Strategy.money_management_strategy_id)
            .distinct()
            .all()
        }


class Strategy(Base, CRUDMixin):
    __tablename__ = "strategy"
    __repr_fields__ = (
        "instrument",
        "annual_roi",
        "max_draw_down",
        "annual_operation_count",
        "money_management_strategy_id",
        "indicator_id",
    )
    __table_args__ = (
        UniqueConstraint(
            "money_management_strategy_id",
            "indicator_id",
            name="uq_mm_strategy_indicator",
        ),
    )

    serialize_rules = (
        "-id",
        "-money_management_strategy",
        "-indicator",
        "-long_operation_points",
        "-short_operation_points",
    )

    query: StrategyQuery = session.query_property(query_cls=StrategyQuery)

    id = Column(Integer, primary_key=True, autoincrement=True)
    instrument = Column(String, nullable=False)
    annual_roi = Column(Float, nullable=False)
    max_draw_down = Column(Float, nullable=False)
    annual_operation_count = Column(Float, nullable=False)
    money_management_strategy_id = Column(
        Integer,
        ForeignKey("money_management_strategy.id"),
        nullable=False,
    )
    indicator_id = Column(
        Integer,
        ForeignKey("indicator.id"),
        nullable=False,
    )

    money_management_strategy: Mapped[MoneyManagementStrategy] = relationship(
        back_populates="strategies"
    )
    indicator: Mapped[Indicator] = relationship(back_populates="strategies")

    long_operation_points: Mapped[list[LongOperationPoint]] = relationship(
        "LongOperationPoint",
        back_populates="strategies",
        secondary="long_operation_points_strategies",
    )
    short_operation_points: Mapped[list[ShortOperationPoint]] = relationship(
        "ShortOperationPoint",
        back_populates="strategies",
        secondary="short_operation_points_strategies",
    )

    def delete(self) -> None:
        object_session(self).delete(self)
        object_session(self).flush()
