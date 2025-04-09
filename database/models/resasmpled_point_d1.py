from __future__ import annotations

from enum import Enum
from typing import Any

from sqlalchemy import Column, Date, Float, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM

from database import Base, CRUDMixin, session


class HighLowOrder(Enum):
    high_first = "high_first"
    low_first = "low_first"
    undefined = "undefined"


class ResampledPointD1Query:
    @staticmethod
    def all() -> list[Any]:
        return list(session.query(ResampledPointD1).all())


class ResampledPointD1(Base, CRUDMixin):
    __tablename__ = "resampled_point_d1"
    __repr_fields__ = ("instrument", "datetime", "high_low_order")
    serialize_rules = ("-id",)

    query = ResampledPointD1Query

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(Date, nullable=False)
    instrument = Column(String, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    high_low_order = Column(PG_ENUM(HighLowOrder), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "datetime",
            "instrument",
            name="uq_datetime_instrument_resampled_d1",
        ),
    )
