from __future__ import annotations

import click
from sqlalchemy import delete

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from database import session
from database.models import RawPointD1, RawPointH1
from logger import log


@click.command("delete", help="Delete Raw Points")
def delete_raw_points() -> None:
    if config.is_production():
        confirm(
            "You are about to delete raw points in production. Do you wish to continue?"
        )

    session.execute(delete(RawPointH1))
    session.execute(delete(RawPointD1))

    session.commit()

    log.info("Deleted raw points")


if __name__ == "__main__":
    delete_raw_points()
