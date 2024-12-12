from __future__ import annotations

import click

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from logger import log


@click.command("delete", help="Delete multiple MoneyManagementStrategy")
def delete_multiple_money_management_strategies() -> None:
    if config.is_production():
        confirm(
            "You are about to delete multiple money management strategies in production. "
            "Do you wish to continue?"
        )

    log.info("Deleted money management strategies")


if __name__ == "__main__":
    delete_multiple_money_management_strategies()
