from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import ARRAY, Column, Date, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, Query, relationship

from database import Base, CRUDMixin, session

if TYPE_CHECKING:
    from database.models import MoneyManagementStrategy, Strategy


class LongOperationPointQuery(Query):
    pass


class LongOperationPoint(Base, CRUDMixin):
    __tablename__ = "long_operation_point"
    __repr_fields__ = ("instrument", "datetime", "money_management_strategy_id")
    __table_args__ = (
        Index(
            "ix_long_operation_point_money_management_strategy_id",
            "money_management_strategy_id",
        ),
    )

    serialize_rules = (
        "-id",
        "-money_management_strategy_id",
        "-money_management_strategy",
        "-strategies",
    )

    query: LongOperationPointQuery = session.query_property(
        query_cls=LongOperationPointQuery
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    instrument = Column(String, nullable=False)
    datetime = Column(Date, nullable=False)
    result = Column(Integer, nullable=False)
    tp = Column(Integer, nullable=False)
    sl = Column(Integer, nullable=False)
    long_balance = Column(ARRAY(Integer), nullable=False)
    risk = Column(Float, nullable=False)
    timestamp = Column(Integer, nullable=False)
    money_management_strategy_id = Column(
        Integer,
        ForeignKey("money_management_strategy.id"),
        nullable=False,
    )

    money_management_strategy: Mapped[MoneyManagementStrategy] = relationship(
        back_populates="long_operation_points",
    )

    strategies: Mapped[list[Strategy]] = relationship(
        "Strategy",
        back_populates="long_operation_points",
        secondary="long_operation_points_strategies",
        cascade="all, delete",
    )

    def to_request_format(self) -> dict[str, Any]:
        return self.to_dict(
            rules=("id", "money_management_strategy_id", "-long_balance", "-datetime")
        )
