"""
Example.

bt mm_strategies delete "atr-1.1-1.4-14" "atr-1.1-1.4-15"
"""

from __future__ import annotations

import click
from sqlalchemy.exc import SQLAlchemyError

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from logger import log
from views.money_management_strategy.delete_multiple_view import (
    MoneyManagementStrategyDeleteMultipleView,
    NonExistentIdentifierError,
)


@click.command("delete", help="Delete multiple MoneyManagementStrategy")
@click.argument("identifiers", nargs=-1)
def delete_multiple_money_management_strategies(identifiers: tuple[str]) -> None:
    if not identifiers:
        confirm(
            "You are about to delete all money management strategies. "
            "Do you wish to continue?"
        )

    if config.is_production():
        confirm(
            "You are about to delete money management strategies in production. "
            "Do you wish to continue?"
        )

    try:
        MoneyManagementStrategyDeleteMultipleView(identifiers=set(identifiers)).run()
    except NonExistentIdentifierError as e:
        log.exception(e)
        err = f"{e}"
        raise click.ClickException(err) from e

    except SQLAlchemyError as e:
        err = f"DB error: {e}"
        log.exception("DB error")
        raise click.ClickException(err) from e

    except Exception as e:
        err = f"Unexpected error: {e}"
        log.exception("Unexpected error")
        raise click.ClickException(err) from e

    log.info("Deleted money management strategies")


if __name__ == "__main__":
    delete_multiple_money_management_strategies()
