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
        self._validate_identifiers()
        self._validate_items()

        return self.items

    def _validate_items(self) -> None:
        if not self.items:
            err = f"Invalid arguments: {self.identifiers=}, " f"{self.items=}"
            raise ValueError(err)

    def _validate_identifiers(self) -> None:
        if self.identifiers:
            existing_identifiers = {item.identifier for item in self.items}
            symmetric_difference = existing_identifiers ^ self.identifiers

            if symmetric_difference:
                err = (
                    "Item identifiers did not match. "
                    f"{self.identifiers=}, {existing_identifiers=}, "
                    f"Symmetric difference: {symmetric_difference}"
                )
                raise ValueError(err)
