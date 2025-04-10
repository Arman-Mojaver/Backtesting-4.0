from sqlalchemy import Column, Float, Integer
from sqlalchemy.orm import Query, object_session

from database import Base, CRUDMixin, session


class StrategyQuery(Query):
    pass


class Strategy(Base, CRUDMixin):
    __tablename__ = "strategy"
    __repr_fields__ = (
        "annual_roi",
        "max_draw_down",
        "annual_operation_count",
        "money_management_strategy_id",
        "indicator_id",
    )
    serialize_rules = (
        "-id",
        "-money_management_strategy_id",
        "-indicator_id",
        "-long_operation_points",
        "-short_operation_points",
    )

    query: StrategyQuery = session.query_property(query_cls=StrategyQuery)

    id = Column(Integer, primary_key=True, autoincrement=True)
    annual_roi = Column(Float, nullable=False)
    max_draw_down = Column(Float, nullable=False)
    annual_operation_count = Column(Float, nullable=False)
    money_management_strategy_id = Column(Integer, nullable=False)
    indicator_id = Column(Integer, nullable=False)

    def delete(self) -> None:
        object_session(self).delete(self)
        object_session(self).flush()
