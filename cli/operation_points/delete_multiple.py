from __future__ import annotations

import click

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from database import session
from database.models import LongOperationPoint, ShortOperationPoint
from logger import log


@click.command("delete", help="Delete multiple Operation Points")
def delete_multiple_operation_points() -> None:
    if config.is_production():
        confirm(
            "You are about to delete operation points in production. "
            "Do you wish to continue?"
        )

    for point in LongOperationPoint.query.all():
        session.delete(point)

    for point in ShortOperationPoint.query.all():
        session.delete(point)

    session.commit()

    log.info("Deleted Operation Points")


if __name__ == "__main__":
    delete_multiple_operation_points()
