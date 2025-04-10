from __future__ import annotations

import click

from cli.resampled_points.create import create_resampled_points
from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from logger import log


@click.command("create", help="Create Strategies")
@click.option("-i", "--instrument", type=str, required=True, help="Instrument")
def create_strategies(instrument: str) -> None:
    instrument = instrument.upper()

    if config.is_production():
        confirm(
            "You are about to create strategies in production. "
            "Do you wish to continue?"
        )

    if instrument not in config.ENABLED_INSTRUMENTS:
        err = f"Instrument not supported: {instrument}. {config.ENABLED_INSTRUMENTS=}"
        raise click.ClickException(err)

    log.info(f"Created strategies for instrument: {instrument}")


if __name__ == "__main__":
    create_resampled_points()
