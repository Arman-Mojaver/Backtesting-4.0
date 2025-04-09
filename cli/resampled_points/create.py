from __future__ import annotations

import click
from sqlalchemy.exc import SQLAlchemyError

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from database import session
from database.handler import DatabaseHandler
from database.models import RawPointD1
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

    # RawPointH1 items also get queried here because the relationship is lazy="subquery"
    raw_points_d1 = RawPointD1.query.all()

    try:
        resampled_points = ResampledPointsCreateMultipleView(
            raw_points_d1=raw_points_d1
        ).run()

    except NoRawPointsError as e:
        err = f"No raw points in database: {e}"
        log.exception("No raw points in database")
        raise click.ClickException(err) from e

    try:
        DatabaseHandler(session=session).commit_resampled_points(
            resampled_points=resampled_points
        )

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
