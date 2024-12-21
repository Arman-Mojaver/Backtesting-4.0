from __future__ import annotations

import click

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from logger import log


@click.command("create", help="Create Operation Points")
def create_operation_points() -> None:
    if config.is_production():
        confirm(
            "You are about to create operation points in production. "
            "Do you wish to continue?"
        )

    log.info("Created operation points")


if __name__ == "__main__":
    create_operation_points()
