from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Column, Float, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import Mapped, Query, object_session, relationship

from database import Base, CRUDMixin, session

if TYPE_CHECKING:
    from database.models import LongOperationPoint, ShortOperationPoint


class MoneyManagementStrategyType(Enum):
    atr = "atr"


class MoneyManagementStrategyQuery(Query):
    def from_ids(self, ids: set[int]) -> Query:
        return self.filter(MoneyManagementStrategy.id.in_(ids))

    def from_identifiers(self, identifiers: set[str]) -> Query:
        return self.filter(MoneyManagementStrategy.identifier.in_(identifiers))


class MoneyManagementStrategy(Base, CRUDMixin):
    __tablename__ = "money_management_strategy"
    __repr_fields__ = ("identifier",)
    serialize_rules = ("-id", "-long_operation_points", "-short_operation_points")

    query: MoneyManagementStrategyQuery = session.query_property(
        query_cls=MoneyManagementStrategyQuery
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(PG_ENUM(MoneyManagementStrategyType), nullable=False)
    tp_multiplier = Column(Float, nullable=False)
    sl_multiplier = Column(Float, nullable=False)
    parameters = Column(JSON, nullable=False)
    identifier = Column(String, nullable=False)
    risk = Column(Float, nullable=False)

    long_operation_points: Mapped[list[LongOperationPoint]] = relationship(
        back_populates="money_management_strategy",
        cascade="all",
        lazy="subquery",
    )
    short_operation_points: Mapped[list[ShortOperationPoint]] = relationship(
        back_populates="money_management_strategy",
        cascade="all",
        lazy="subquery",
    )

    __table_args__ = (
        UniqueConstraint("identifier", name="uq_money_management_strategy_identifier"),
    )

    def delete(self) -> None:
        object_session(self).delete(self)
        object_session(self).flush()
