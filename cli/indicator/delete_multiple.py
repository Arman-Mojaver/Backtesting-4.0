"""
Example.

bt indicators delete "macd.sma-12-close,ema-5-close" "macd.sma-12-close,ema-6-close"
"""

from __future__ import annotations

import click
from sqlalchemy.exc import SQLAlchemyError

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from database import session
from database.handler import DatabaseHandler
from database.models import Indicator
from logger import log
from views.delete_multiple_validator import DeleteMultipleValidator


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
        queried_indicators = Indicator.query.from_identifiers(
            identifiers=set(identifiers)
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
        indicators = DeleteMultipleValidator(
            identifiers=set(identifiers),
            items=queried_indicators,
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
        DatabaseHandler(session=session).delete_indicators(indicators=indicators)

    except SQLAlchemyError as e:
        err = f"DB error: {e}"
        log.exception("DB error")
        raise click.ClickException(err) from e

    except Exception as e:
        err = f"Unexpected error: {e}"
        log.exception("Unexpected error")
        raise click.ClickException(err) from e

    log.info(f"Deleted indicators. Count: {len(indicators)}")


if __name__ == "__main__":
    delete_multiple_indicators()
