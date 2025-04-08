from __future__ import annotations

import click
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from database import session
from database.handler import DatabaseHandler
from logger import log
from views.raw_points.raw_points_view import RawPointsCreateMultipleView
from views.raw_points.utils import LoadFileData


@click.command("create", help="Create Raw Points")
def create_raw_points() -> None:
    if config.is_production():
        confirm(
            "You are about to create raw points in production. Do you wish to continue?"
        )

    try:
        file_data = LoadFileData().run()

    except FileNotFoundError as e:
        err = f"File not found: {e}"
        log.exception("File not found")
        raise click.ClickException(err) from e

    try:
        raw_points_d1 = RawPointsCreateMultipleView(
            data=file_data,
            enabled_instruments=config.ENABLED_INSTRUMENTS,
        ).run()

    except ValidationError as e:
        err = f"Validation error: {e}"
        log.exception("Validation error")
        raise click.ClickException(err) from e

    try:
        DatabaseHandler(session=session).commit_raw_points(
            raw_points_d1=raw_points_d1
        )

    except SQLAlchemyError as e:
        err = f"DB error: {e}"
        log.exception("DB error")
        raise click.ClickException(err) from e

    except Exception as e:
        err = f"Unexpected error: {e}"
        log.exception("Unexpected error")
        raise click.ClickException(err) from e

    log.info("Created raw points")


if __name__ == "__main__":
    create_raw_points()
