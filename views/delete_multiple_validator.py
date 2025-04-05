from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.models import Indicator, MoneyManagementStrategy


class DeleteMultipleValidator:
    def __init__(
        self,
        identifiers: set[str],
        items: list[MoneyManagementStrategy] | list[Indicator],
    ):
        self.identifiers: set[str] = identifiers
        self.items: list[MoneyManagementStrategy] | list[Indicator] = items

    def run(self) -> list[MoneyManagementStrategy] | list[Indicator]:
        self._validate_arguments()
        self._validates_identifiers_are_equal()

        return self.items

    def _validate_arguments(self):
        if not (self.identifiers and self.items):
            err = f"Invalid arguments: {self.identifiers}, " f"{self.items}"
            raise ValueError(err)

    def _validates_identifiers_are_equal(self):
        existing_identifiers = {item.identifier for item in self.items}
        symmetric_difference = existing_identifiers ^ self.identifiers

        if symmetric_difference:
            err = (
                "MoneyManagementStrategy identifiers did not match. "
                f"Symmetric difference: {symmetric_difference}"
            )
            raise ValueError(err)
