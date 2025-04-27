from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any

from pydantic import ValidationError
from sqlalchemy import JSON, Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, Query, object_session, relationship

from database import Base, CRUDMixin, session
from schemas.indicator import MacdParametersSchema, RsiParametersSchema

if TYPE_CHECKING:
    from database.models import Strategy


class IndicatorType(Enum):
    macd = "macd"
    rsi = "rsi"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]


PARAMETERS_VALIDATOR_MAPPER = {
    IndicatorType.macd: MacdParametersSchema,
    IndicatorType.rsi: RsiParametersSchema,
}


class IndicatorQuery(Query):
    def from_ids(self, ids: set[int]) -> IndicatorQuery:
        return self.filter(Indicator.id.in_(ids))

    def from_identifiers(self, identifiers: set[str]) -> IndicatorQuery:
        return self.filter(Indicator.identifier.in_(identifiers))


class Indicator(Base, CRUDMixin):
    __tablename__ = "indicator"
    __repr_fields__ = ("identifier",)
    serialize_rules = ("-id", "-strategies")

    query: IndicatorQuery = session.query_property(query_cls=IndicatorQuery)

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    parameters = Column(JSON, nullable=False)
    identifier = Column(String, nullable=False)

    strategies: Mapped[list[Strategy]] = relationship(
        back_populates="indicator",
        cascade="all",
    )

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

    def to_dict_with_ids(self) -> dict[str, Any]:
        return self.to_dict(rules=("id",))
