from __future__ import annotations

import click
from sqlalchemy.exc import SQLAlchemyError

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from logger import log
from views.resampled_points_view import (
    NoRawPointsError,
    ResampledPointsCreateMultipleView,
)


@click.command("create", help="Create Resampled Points")
def create_resampled_points() -> None:
    if config.is_production():
        confirm(
            "You are about to create resampled points in production. "
            "Do you wish to continue?"
        )

    try:
        ResampledPointsCreateMultipleView().run()

    except NoRawPointsError as e:
        err = f"No raw points in database: {e}"
        log.exception("No raw points in database")
        raise click.ClickException(err) from e

    except SQLAlchemyError as e:
        err = f"DB error: {e}"
        log.exception("DB error")
        raise click.ClickException(err) from e

    except Exception as e:
        err = f"Unexpected error: {e}"
        log.exception("Unexpected error")
        raise click.ClickException(err) from e

    log.info("Created resampled points")


if __name__ == "__main__":
    create_resampled_points()
