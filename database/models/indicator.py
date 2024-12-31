from __future__ import annotations

from enum import Enum
from typing import Any

from sqlalchemy import JSON, Column, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import object_session

from database import Base, CRUDMixin, session


class IndicatorType(Enum):
    macd = "macd"


class IndicatorQuery:
    @staticmethod
    def all() -> list[Any]:
        return list(session.query(Indicator).all())


class Indicator(Base, CRUDMixin):
    __tablename__ = "indicator"
    __repr_fields__ = ("identifier",)
    serialize_rules = ("-id",)

    query = IndicatorQuery

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(PG_ENUM(IndicatorType), nullable=False)
    parameters = Column(JSON, nullable=False)
    identifier = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("identifier", name="uq_indicator_identifier"),)

    def delete(self) -> None:
        object_session(self).delete(self)
        object_session(self).flush()
