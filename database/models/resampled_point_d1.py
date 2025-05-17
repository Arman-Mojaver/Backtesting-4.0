from __future__ import annotations

from enum import Enum
from typing import Any

from sqlalchemy import Column, Date, Float, Index, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import Query

from database import Base, CRUDMixin, session
from utils.date_utils import string_to_datetime


class HighLowOrder(Enum):
    high_first = "high_first"
    low_first = "low_first"
    undefined = "undefined"


class ResampledPointD1List(list):
    def to_request_format(self) -> list[dict[str, Any]]:
        return [item.to_request_format() for item in self]


class ResampledPointD1Query(Query):
    def from_instrument(self, instrument: str) -> ResampledPointD1Query:
        return self.filter_by(instrument=instrument)


class ResampledPointD1(Base, CRUDMixin):
    __tablename__ = "resampled_point_d1"
    __repr_fields__ = ("instrument", "datetime", "high_low_order")
    __table_args__ = (
        UniqueConstraint(
            "datetime",
            "instrument",
            name="uq_datetime_instrument_resampled_d1",
        ),
        Index("ix_resampled_point_d1_instrument", "instrument"),
    )

    serialize_rules = ("-id",)

    query: ResampledPointD1Query = session.query_property(query_cls=ResampledPointD1Query)

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(Date, nullable=False)
    instrument = Column(String, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    high_low_order = Column(PG_ENUM(HighLowOrder), nullable=False)
    timestamp = Column(Integer, nullable=False)

    def to_request_format(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "datetime": str(self.datetime),
            "instrument": self.instrument,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "high_low_order": HighLowOrder(self.high_low_order).value,
            "timestamp": int(string_to_datetime(str(self.datetime)).timestamp()),
        }
