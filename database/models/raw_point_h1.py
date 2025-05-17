from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, Query, relationship

from database import Base, CRUDMixin, session

if TYPE_CHECKING:
    from database.models import RawPointD1


class RawPointH1Query(Query):
    pass


class RawPointH1(Base, CRUDMixin):
    __tablename__ = "raw_point_h1"
    __repr_fields__ = ("instrument", "datetime")
    __table_args__ = (
        UniqueConstraint("datetime", "instrument", name="uq_datetime_instrument_h1"),
        Index("ix_raw_point_h1_instrument", "instrument"),
    )

    serialize_rules = ("-id", "-raw_point_d1_id", "-raw_point_d1")

    query: RawPointH1Query = session.query_property(query_cls=RawPointH1Query)

    id = Column(Integer, primary_key=True, autoincrement=True)
    raw_point_d1_id = Column(Integer, ForeignKey("raw_point_d1.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    instrument = Column(String, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)

    raw_point_d1: Mapped[RawPointD1] = relationship(back_populates="raw_points_h1")
