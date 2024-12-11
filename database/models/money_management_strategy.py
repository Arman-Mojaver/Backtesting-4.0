from __future__ import annotations

from enum import Enum
from typing import Any

from sqlalchemy import JSON, Column, Float, Integer
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import object_session

from database import Base, CRUDMixin, session


class MoneyManagementStrategyType(Enum):
    atr = "atr"


class MoneyManagementStrategyQuery:
    @staticmethod
    def all() -> list[Any]:
        return list(session.query(MoneyManagementStrategy).all())


class MoneyManagementStrategy(Base, CRUDMixin):
    __tablename__ = "money_management_strategy"
    __repr_fields__ = ("type", "tp_multiplier", "sl_multiplier", "parameters")
    serialize_rules = ("-id",)

    query = MoneyManagementStrategyQuery

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(PG_ENUM(MoneyManagementStrategyType), nullable=False)
    tp_multiplier = Column(Float, nullable=False)
    sl_multiplier = Column(Float, nullable=False)
    parameters = Column(JSON, nullable=False)

    def delete(self) -> None:
        object_session(self).delete(self)
        object_session(self).flush()
