from __future__ import annotations

import click

from cli.resampled_points.create import create_resampled_points
from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from logger import log


@click.command("create", help="Create Strategies")
@click.option("-i", "--instrument", type=str, required=True, help="Instrument")
def create_strategies(instrument: str) -> None:
    if config.is_production():
        confirm(
            "You are about to create strategies in production. "
            "Do you wish to continue?"
        )

    log.info(f"Created strategies for instrument: {instrument}")


if __name__ == "__main__":
    create_resampled_points()
