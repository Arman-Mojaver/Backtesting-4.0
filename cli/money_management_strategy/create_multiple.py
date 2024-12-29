"""
Example.

bt mm_strategies create -tp 1.5 1.5 -sl 1.0 1.0 -atr 14 14
"""

from __future__ import annotations

import click
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from logger import log
from utils.range_utils import InvalidRangeInputsError
from views.money_management_strategy.create_multiple_view import (
    MoneyManagementStrategyCreateMultipleView,
)


@click.command("create", help="Create multiple MoneyManagementStrategy")
@click.option(
    "-t",
    "--type",
    type=str,
    default="atr",
    help="Money Management Strategy type",
)
@click.option(
    "-tp",
    "--tp_multiplier_range",
    type=click.Tuple([float, float]),
    help="TP Multiplier range",
)
@click.option(
    "-sl",
    "--sl_multiplier_range",
    type=click.Tuple([float, float]),
    help="SL Multiplier range",
)
@click.option(
    "-atr",
    "--atr_parameter_range",
    type=click.Tuple([int, int]),
    help="ATR parameter range",
)
@click.option(
    "-e",
    "--example",
    type=bool,
    is_flag=True,
    default=False,
    help="Display an example of how to use the command",
)
def create_multiple_money_management_strategies(
    type: str,  # noqa: A002
    tp_multiplier_range: tuple[float, float],
    sl_multiplier_range: tuple[float, float],
    atr_parameter_range: tuple[int, int],
    *,
    example: bool,
) -> None:
    if example:
        click.echo("bt mm_strategies create -tp 1.5 1.5 -sl 1.0 1.0 -atr 14 14")
        return

    if not all([type, tp_multiplier_range, sl_multiplier_range, atr_parameter_range]):
        err = (
            f"Missing options: {type=}, {tp_multiplier_range=}, "
            f"{sl_multiplier_range=}, {atr_parameter_range=}"
        )
        raise click.ClickException(err)

    if config.is_production():
        confirm(
            "You are about to create multiple money management strategies in production. "
            "Do you wish to continue?"
        )

    try:
        MoneyManagementStrategyCreateMultipleView(
            type=type,
            tp_multiplier_range=tp_multiplier_range,
            sl_multiplier_range=sl_multiplier_range,
            atr_parameter_range=atr_parameter_range,
        ).run()

    except InvalidRangeInputsError as e:
        err = f"Invalid range input: {e}"
        log.exception("Invalid range input")
        raise click.ClickException(err) from e

    except ValidationError as e:
        err = f"Validation error: {e}"
        log.exception("Validation error")
        raise click.ClickException(err) from e

    except SQLAlchemyError as e:
        err = f"DB error: {e}"
        log.exception("DB error")
        raise click.ClickException(err) from e

    except Exception as e:
        err = f"Unexpected error: {e}"
        log.exception("Unexpected error")
        raise click.ClickException(err) from e

    log.info("Created money management strategies")


if __name__ == "__main__":
    create_multiple_money_management_strategies()
