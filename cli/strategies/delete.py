from __future__ import annotations

import click
from sqlalchemy import delete

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from database import session
from database.models import Strategy
from logger import log


@click.command("delete", help="Delete Strategies")
def delete_strategies() -> None:
    if config.is_production():
        confirm(
            "You are about to delete strategies in production. "
            "Do you wish to continue?"
        )

    session.execute(delete(Strategy))
    session.commit()

    log.info("Deleted strategies")


if __name__ == "__main__":
    delete_strategies()
