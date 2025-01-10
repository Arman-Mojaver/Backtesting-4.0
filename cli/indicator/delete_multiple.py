"""
Example.

bt indicators delete "macd.sma-12-close,ema-5-close" "macd.sma-12-close,ema-6-close"
"""

from __future__ import annotations

import click
from sqlalchemy.exc import SQLAlchemyError

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from logger import log
from views.indicator.delete_multiple_view import (
    IndicatorDeleteMultipleView,
    NonExistentIdentifierError,
)


@click.command("delete", help="Delete multiple Indicator")
@click.argument("identifiers", nargs=-1)
def delete_multiple_indicators(identifiers: tuple[str]) -> None:
    if not identifiers:
        confirm("You are about to delete all indicators. Do you wish to continue?")

    if config.is_production():
        confirm(
            "You are about to delete indicators in production. "
            "Do you wish to continue?"
        )

    try:
        IndicatorDeleteMultipleView(identifiers=set(identifiers)).run()

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

    log.info("Deleted indicators")


if __name__ == "__main__":
    delete_multiple_indicators()
