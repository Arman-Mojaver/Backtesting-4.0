from __future__ import annotations

from collections import defaultdict
from typing import Any

from sqlalchemy import Column, DateTime, Float, Integer, String, UniqueConstraint

from database import Base, CRUDMixin, session


class MultipleValuesError(Exception):
    """Error raised when there are multiple values for the same key."""


class RawPointH1Query:
    @staticmethod
    def all() -> list[Any]:
        return list(session.query(RawPointH1).all())

    @staticmethod
    def dict_by_key(key: str = "id") -> dict[Any, Any]:
        values = [
            getattr(obj, key)
            for obj in session.query(RawPointH1).all()
            if getattr(obj, key)
        ]
        if len(values) != len(set(values)):
            err = f"There where duplicated keys: {values}"
            raise MultipleValuesError(err)

        dictionary: dict[Any, Any] = defaultdict()
        for obj in session.query(RawPointH1).all():
            dictionary[getattr(obj, key)] = obj

        return dictionary

    @staticmethod
    def dict_multi_by_key(key: str) -> dict[str, list[Any]]:
        dictionary = defaultdict(list)
        for obj in session.query(RawPointH1).all():
            dictionary[getattr(obj, key)].append(obj)

        return dictionary


class RawPointH1(Base, CRUDMixin):
    __tablename__ = "raw_point_h1"
    __repr_fields__ = ("instrument", "datetime")
    serialize_rules = ("-id",)

    query = RawPointH1Query

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False)
    instrument = Column(String, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("datetime", "instrument", name="uq_datetime_instrument_h1"),
    )
