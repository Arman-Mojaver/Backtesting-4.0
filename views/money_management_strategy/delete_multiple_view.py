from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.exc import SQLAlchemyError

from config.logging_config.log_decorators import log_on_end, log_on_start
from database import session
from database.models import MoneyManagementStrategy

if TYPE_CHECKING:
    from sqlalchemy.orm import Query


class NonExistentIdentifierError(Exception):
    pass


class MoneyManagementStrategyDeleteMultipleView:
    def __init__(self, identifiers: set[str] | None = None):
        self.identifiers: set[str] | None = identifiers or set()
        self.query: Query = session.query(MoneyManagementStrategy)
        self.money_management_strategies: list[MoneyManagementStrategy] = []

    @log_on_end("Finished MoneyManagementStrategyDeleteMultipleView")
    def run(self) -> None:
        self._filter_by_identifiers()
        self.money_management_strategies = self.query.all()
        self._validate_identifiers()
        self._delete_money_management_strategies()
        self._commit()

    def _filter_by_identifiers(self) -> None:
        if self.identifiers:
            self.query = self.query.filter(
                MoneyManagementStrategy.identifier.in_(self.identifiers)
            )

    def _validate_identifiers(self) -> None:
        identifiers = self._get_queried_identifiers()

        if self.identifiers and set(self.identifiers) != set(identifiers):
            err = (
                "Identifier mismatch: Introduced identifiers: "
                f"{self.identifiers}, Existing Identifiers: {identifiers}"
            )
            raise NonExistentIdentifierError(err)

    def _get_queried_identifiers(self) -> set[str]:
        return {
            money_management_strategy.identifier
            for money_management_strategy in self.money_management_strategies
        }

    @log_on_start("Deleting MoneyManagementStrategy")
    def _delete_money_management_strategies(self) -> None:
        for money_management_strategy in self.money_management_strategies:
            session.delete(money_management_strategy)

    @staticmethod
    @log_on_end("Committed")
    def _commit() -> None:
        try:
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
