from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.models import MoneyManagementStrategy


class MoneyManagementStrategyDeleteMultipleView:
    def __init__(
        self,
        identifiers: set[str],
        money_management_strategies: list[MoneyManagementStrategy],
    ):
        self.identifiers: set[str] = identifiers
        self.money_management_strategies: list[MoneyManagementStrategy] = (
            money_management_strategies
        )

    def run(self) -> list[MoneyManagementStrategy]:
        self._validate_arguments()
        self._validates_identifiers_are_equal()

        return self.money_management_strategies

    def _validate_arguments(self):
        if not (self.identifiers and self.money_management_strategies):
            err = (
                f"Invalid arguments: {self.identifiers}, "
                f"{self.money_management_strategies}"
            )
            raise ValueError(err)

    def _validates_identifiers_are_equal(self):
        existing_identifiers = {
            item.identifier for item in self.money_management_strategies
        }
        symmetric_difference = existing_identifiers ^ self.identifiers

        if symmetric_difference:
            err = (
                "MoneyManagementStrategy identifiers did not match. "
                f"Symmetric difference: {symmetric_difference}"
            )
            raise ValueError(err)
