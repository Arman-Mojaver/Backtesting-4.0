from __future__ import annotations

from collections import defaultdict
from enum import Enum
from typing import Any

from sqlalchemy import Column, Date, Float, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM

from database import Base, CRUDMixin, session


class MultipleValuesError(Exception):
    """Error raised when there are multiple values for the same key."""


class HighLowOrder(Enum):
    high_first = "high_first"
    low_first = "low_first"
    undefined = "undefined"


class ResampledPointD1Query:
    @staticmethod
    def all() -> list[Any]:
        return list(session.query(ResampledPointD1).all())

    @staticmethod
    def dict_by_key(key: str = "id") -> dict[Any, Any]:
        values = [
            getattr(obj, key)
            for obj in session.query(ResampledPointD1).all()
            if getattr(obj, key)
        ]
        if len(values) != len(set(values)):
            err = f"There where duplicated keys: {values}"
            raise MultipleValuesError(err)

        dictionary: dict[Any, Any] = defaultdict()
        for obj in session.query(ResampledPointD1).all():
            dictionary[getattr(obj, key)] = obj

        return dictionary

    @staticmethod
    def dict_multi_by_key(key: str) -> dict[str, list[Any]]:
        dictionary = defaultdict(list)
        for obj in session.query(ResampledPointD1).all():
            dictionary[getattr(obj, key)].append(obj)

        return dictionary


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
