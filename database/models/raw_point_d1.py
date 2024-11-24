from sqlalchemy import Column, Date, Float, Integer, String, UniqueConstraint

from database import Base, CRUDMixin


class RawPointD1(Base, CRUDMixin):
    __tablename__ = "raw_point_d1"
    __repr_fields__ = ("instrument", "datetime")
    serialize_rules = ("-id",)

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(Date, nullable=False)
    instrument = Column(String, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("datetime", "instrument", name="uq_datetime_instrument"),
    )
