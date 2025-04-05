"""
Example.

bt mm_strategies delete "atr-1.1-1.4-14-0.02" "atr-1.1-1.4-15-0.02"
"""

from __future__ import annotations

import click
from sqlalchemy.exc import SQLAlchemyError

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from database import session
from database.handler import DatabaseHandler
from database.models import MoneyManagementStrategy
from logger import log
from views.money_management_strategy.delete_multiple_view import (
    MoneyManagementStrategyDeleteMultipleView,
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
        queried_money_management_strategies = (
            MoneyManagementStrategy.query.from_identifiers(identifiers=set(identifiers))
        )

    except SQLAlchemyError as e:
        err = f"DB error: {e}"
        log.exception("DB error")
        raise click.ClickException(err) from e

    except Exception as e:
        err = f"Unexpected error: {e}"
        log.exception("Unexpected error")
        raise click.ClickException(err) from e

    try:
        money_management_strategies = MoneyManagementStrategyDeleteMultipleView(
            identifiers=set(identifiers),
            money_management_strategies=queried_money_management_strategies,
        ).run()

    except ValueError as e:
        log.exception(e)
        err = f"{e}"
        raise click.ClickException(err) from e

    except Exception as e:
        err = f"Unexpected error: {e}"
        log.exception("Unexpected error")
        raise click.ClickException(err) from e

    try:
        DatabaseHandler(session=session).delete_money_management_strategies(
            money_management_strategies=money_management_strategies
        )

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
