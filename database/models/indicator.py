from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import ValidationError
from sqlalchemy import JSON, Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import object_session

from database import Base, CRUDMixin, session
from schemas.indicator.macd_schema import MacdParametersSchema


class IndicatorType(Enum):
    macd = "macd"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]


PARAMETERS_VALIDATOR_MAPPER = {IndicatorType.macd: MacdParametersSchema}


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
    type = Column(String, nullable=False)
    parameters = Column(JSON, nullable=False)
    identifier = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("identifier", name="uq_indicator_identifier"),)

    def __init__(self, **kwargs: Any):  # noqa: ANN401
        super().__init__(**kwargs)

        self._validate_type()
        self._validate_parameters()

    def _validate_type(self):
        if self.type not in IndicatorType.values():
            err = f"Missing or invalid type: {self.type}"
            raise TypeError(err)

    def _validate_parameters(self):
        schema = PARAMETERS_VALIDATOR_MAPPER[IndicatorType(self.type)]
        try:
            schema(**self.to_dict())
        except ValidationError:
            raise

    def delete(self) -> None:
        object_session(self).delete(self)
        object_session(self).flush()
