from __future__ import annotations

from enum import Enum
from typing import Any

from sqlalchemy import JSON, Column, Float, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import object_session

from database import Base, CRUDMixin, session


class MoneyManagementStrategyType(Enum):
    atr = "atr"


class NonExistentIdError(Exception):
    pass


class NonExistentIdentifierError(Exception):
    pass


class MoneyManagementStrategyQuery:
    @staticmethod
    def all() -> list[Any]:
        return list(session.query(MoneyManagementStrategy).all())

    @staticmethod
    def from_ids(ids: set[int]) -> list[MoneyManagementStrategy]:
        if not ids:
            err = "No ids introduced"
            raise NonExistentIdError(err)

        items = list(
            session.query(MoneyManagementStrategy)
            .filter(MoneyManagementStrategy.id.in_(ids))
            .all()
        )

        missing_ids = ids - {item.id for item in items}
        if missing_ids:
            err = f"Missing ids: {missing_ids}"
            raise NonExistentIdError(err)

        return items

    @staticmethod
    def from_identifiers(identifiers: set[int]) -> list[MoneyManagementStrategy]:
        if not identifiers:
            err = "No identifiers introduced"
            raise NonExistentIdentifierError(err)

        items = list(
            session.query(MoneyManagementStrategy)
            .filter(MoneyManagementStrategy.identifier.in_(identifiers))
            .all()
        )

        missing_identifiers = identifiers - {item.identifier for item in items}
        if missing_identifiers:
            err = f"Missing missing_identifiers: {missing_identifiers}"
            raise NonExistentIdentifierError(err)

        return items


class MoneyManagementStrategy(Base, CRUDMixin):
    __tablename__ = "money_management_strategy"
    __repr_fields__ = ("identifier",)
    serialize_rules = ("-id",)

    query = MoneyManagementStrategyQuery

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(PG_ENUM(MoneyManagementStrategyType), nullable=False)
    tp_multiplier = Column(Float, nullable=False)
    sl_multiplier = Column(Float, nullable=False)
    parameters = Column(JSON, nullable=False)
    identifier = Column(String, nullable=False)
    risk = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("identifier", name="uq_money_management_strategy_identifier"),
    )

    def delete(self) -> None:
        object_session(self).delete(self)
        object_session(self).flush()

    def __eq__(self, other: MoneyManagementStrategy) -> bool:
        return self.to_dict() == other.to_dict()
