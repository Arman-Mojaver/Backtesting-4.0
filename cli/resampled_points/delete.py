from __future__ import annotations

import click

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from database import session
from database.models import ResampledPointD1
from logger import log


@click.command("delete", help="Delete Resampled Points")
def delete_resampled_points() -> None:
    if config.is_production():
        confirm(
            "You are about to delete resampled points in production. "
            "Do you wish to continue?"
        )

    for point in ResampledPointD1.query.all():
        session.delete(point)

    session.commit()

    log.info("Deleted resampled points")


if __name__ == "__main__":
    delete_resampled_points()
