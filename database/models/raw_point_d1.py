from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Any

from sqlalchemy import Column, Date, Float, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from database import Base, CRUDMixin, session
from database.models.resasmpled_point_d1 import HighLowOrder

if TYPE_CHECKING:
    from database.models import RawPointH1


class MultipleValuesError(Exception):
    """Error raised when there are multiple values for the same key."""


class RawPointD1Query:
    @staticmethod
    def all() -> list[Any]:
        return list(session.query(RawPointD1).all())

    @staticmethod
    def dict_by_key(key: str = "id") -> dict[Any, Any]:
        values = [
            getattr(obj, key)
            for obj in session.query(RawPointD1).all()
            if getattr(obj, key)
        ]
        if len(values) != len(set(values)):
            err = f"There where duplicated keys: {values}"
            raise MultipleValuesError(err)

        dictionary: dict[Any, Any] = defaultdict()
        for obj in session.query(RawPointD1).all():
            dictionary[getattr(obj, key)] = obj

        return dictionary

    @staticmethod
    def dict_multi_by_key(key: str) -> dict[str, list[Any]]:
        dictionary = defaultdict(list)
        for obj in session.query(RawPointD1).all():
            dictionary[getattr(obj, key)].append(obj)

        return dictionary


class RawPointD1(Base, CRUDMixin):
    __tablename__ = "raw_point_d1"
    __repr_fields__ = ("instrument", "datetime")
    serialize_rules = ("-id", "-raw_points_h1")

    query = RawPointD1Query

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(Date, nullable=False)
    instrument = Column(String, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)

    raw_points_h1: Mapped[list[RawPointH1]] = relationship(
        back_populates="raw_point_d1",
        cascade="all",
    )

    __table_args__ = (
        UniqueConstraint("datetime", "instrument", name="uq_datetime_instrument_d1"),
    )

    def _max_high_raw_point_h1(self) -> RawPointH1:
        return max(self.raw_points_h1, key=lambda point: point.high)

    def _min_low_raw_point_h1(self) -> RawPointH1:
        return min(self.raw_points_h1, key=lambda point: point.low)

    def high_low_order(self) -> HighLowOrder:
        if self._max_high_raw_point_h1().datetime < self._min_low_raw_point_h1().datetime:
            return HighLowOrder.high_first

        if self._max_high_raw_point_h1().datetime > self._min_low_raw_point_h1().datetime:
            return HighLowOrder.low_first

        return HighLowOrder.undefined
